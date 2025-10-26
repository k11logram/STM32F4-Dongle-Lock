/* USER CODE BEGIN Header */
/**
  ******************************************************************************
  * @file           : main.c
  * @brief          : Main program body 
  ******************************************************************************
  * @attention
  *
  * Copyright (c) 2025 STMicroelectronics.
  * All rights reserved.
  *
  * This software is licensed under terms that can be found in the LICENSE file
  * in the root directory of this software component.
  * If no LICENSE file comes with this software, it is provided AS-IS.
  *
  ******************************************************************************
  */
/* USER CODE END Header */

#include "main.h"
#include "lcd_stm32f4.h"
#include <stdio.h>
#include <string.h>

/* USER CODE BEGIN Includes */
UART_HandleTypeDef huart1;
/* USER CODE END Includes */

/* USER CODE BEGIN PTD */
typedef enum {
    LED_MODE_NONE,
    LED_MODE_ALL_ON,
    LED_MODE_BLINK_ALL,
    LED_MODE_BLINK_ODD,
    LED_MODE_SINGLE
} LED_Mode;
/* USER CODE END PTD */

/* USER CODE BEGIN PD */
#define BLINK_INTERVAL 500  // ms
#define LED_PINS (GPIO_PIN_0|GPIO_PIN_1|GPIO_PIN_2|GPIO_PIN_3| \
                  GPIO_PIN_4|GPIO_PIN_5|GPIO_PIN_6|GPIO_PIN_7)
#define MAX_CODE_LENGTH 19
#define RX_BUFFER_SIZE 64
#define CMD_TIMEOUT 3000  // Return to idle after 3 seconds
/* USER CODE END PD */

/* USER CODE BEGIN PV */
char access_code[3][MAX_CODE_LENGTH + 1] = {"", "", ""};
volatile char rx_buffer[RX_BUFFER_SIZE];
volatile uint8_t rx_index = 0;
volatile uint8_t cmd_ready = 0;
uint8_t byte;

LED_Mode led_mode = LED_MODE_NONE;
LED_Mode idle_led_mode = LED_MODE_BLINK_ALL;
uint8_t single_led = 0;
uint32_t last_toggle = 0;
uint32_t last_cmd_time = 0;
uint8_t blink_state = 0;
/* USER CODE END PV */

/* Private function prototypes -----------------------------------------------*/
void SystemClock_Config(void);
static void MX_GPIO_Init(void);
static void MX_USART1_UART_Init(void);
void send_message(const char *msg);
void process_command(const char *cmd);

/* USER CODE BEGIN PFP */
void leds_all_on(void);
void leds_all_off(void);
void leds_blink_all(void);
void leds_blink_odd(void);
void leds_update(void);
void leds_set(uint8_t pin);
void check_led_timeout(void);
/* USER CODE END PFP */

/* USER CODE BEGIN 0 */
/* LED CONTROL ---------------------------------------------------------*/
void leds_all_on(void) {
    HAL_GPIO_WritePin(GPIOB, LED_PINS, GPIO_PIN_SET);
}

void leds_all_off(void) {
    HAL_GPIO_WritePin(GPIOB, LED_PINS, GPIO_PIN_RESET);
}

void leds_set(uint8_t pin) {
    leds_all_off();
    if (pin < 8) {
        HAL_GPIO_WritePin(GPIOB, (1 << pin), GPIO_PIN_SET);
    }
}

void leds_blink_all(void) {
    uint32_t now = HAL_GetTick();
    if (now - last_toggle >= BLINK_INTERVAL) {
        blink_state = !blink_state;
        if (blink_state) leds_all_on();
        else leds_all_off();
        last_toggle = now;
    }
}

void leds_blink_odd(void) {
    uint32_t now = HAL_GetTick();
    if (now - last_toggle >= BLINK_INTERVAL) {
        blink_state = !blink_state;
        for (uint8_t i = 0; i < 8; i++) {
            if (i % 2 == 1)
                HAL_GPIO_WritePin(GPIOB, (1 << i),
                    blink_state ? GPIO_PIN_SET : GPIO_PIN_RESET);
            else
                HAL_GPIO_WritePin(GPIOB, (1 << i), GPIO_PIN_RESET);
        }
        last_toggle = now;
    }
}

void leds_update(void) {
    switch (led_mode) {
        case LED_MODE_ALL_ON:
            leds_all_on();
            break;
        case LED_MODE_BLINK_ALL:
            leds_blink_all();
            break;
        case LED_MODE_BLINK_ODD:
            leds_blink_odd();
            break;
        case LED_MODE_SINGLE:
            leds_set(single_led);
            break;
        default:
            leds_all_off();
            break;
    }
}

void check_led_timeout(void) {
    uint32_t now = HAL_GetTick();
    if (led_mode == LED_MODE_SINGLE && (now - last_cmd_time >= CMD_TIMEOUT)) {
        led_mode = idle_led_mode;
    }
}
/* USER CODE END 0 */

/* MAIN ----------------------------------------------------------------------*/
int main(void)
{
  HAL_Init();
  SystemClock_Config();
  MX_GPIO_Init();
  MX_USART1_UART_Init();

  /* LCD & STARTUP DISPLAY */
  // init_LCD();
  // HAL_Delay(100);
  // lcd_command(CLEAR);
  // HAL_Delay(10);
  // lcd_command(DISPLAY_ON);
  // HAL_Delay(5);
  // lcd_putstring("STM DONGLE LOCK");
  // HAL_Delay(50);
  // lcd_command(LINE_TWO);
  // HAL_Delay(5);
  // lcd_putstring("Ready...");
  // HAL_Delay(1000);

  leds_all_on();
  led_mode = LED_MODE_ALL_ON;
  HAL_Delay(1000);

  HAL_UART_Receive_IT(&huart1, &byte, 1);
  send_message("STM Ready");

  char local_buffer[RX_BUFFER_SIZE];

  while (1)
  {
      // Check if command is ready to process
      if (cmd_ready) {
          __disable_irq();
          strncpy(local_buffer, (char *)rx_buffer, RX_BUFFER_SIZE - 1);
          local_buffer[RX_BUFFER_SIZE - 1] = '\0';
          cmd_ready = 0;
          __enable_irq();

          process_command(local_buffer);
      }

      leds_update();
      check_led_timeout();
      HAL_Delay(10);
  }
}

/* CLOCK CONFIG ---------------------------------------------------------------*/
void SystemClock_Config(void)
{
  RCC_OscInitTypeDef RCC_OscInitStruct = {0};
  RCC_ClkInitTypeDef RCC_ClkInitStruct = {0};

  __HAL_RCC_PWR_CLK_ENABLE();
  __HAL_PWR_VOLTAGESCALING_CONFIG(PWR_REGULATOR_VOLTAGE_SCALE3);

  RCC_OscInitStruct.OscillatorType = RCC_OSCILLATORTYPE_HSI;
  RCC_OscInitStruct.HSIState = RCC_HSI_ON;
  RCC_OscInitStruct.HSICalibrationValue = RCC_HSICALIBRATION_DEFAULT;
  RCC_OscInitStruct.PLL.PLLState = RCC_PLL_NONE;

  if (HAL_RCC_OscConfig(&RCC_OscInitStruct) != HAL_OK)
      Error_Handler();

  RCC_ClkInitStruct.ClockType = RCC_CLOCKTYPE_HCLK|RCC_CLOCKTYPE_SYSCLK
                              |RCC_CLOCKTYPE_PCLK1|RCC_CLOCKTYPE_PCLK2;
  RCC_ClkInitStruct.SYSCLKSource = RCC_SYSCLKSOURCE_HSI;
  RCC_ClkInitStruct.AHBCLKDivider = RCC_SYSCLK_DIV1;
  RCC_ClkInitStruct.APB1CLKDivider = RCC_HCLK_DIV1;
  RCC_ClkInitStruct.APB2CLKDivider = RCC_HCLK_DIV1;

  if (HAL_RCC_ClockConfig(&RCC_ClkInitStruct, FLASH_LATENCY_0) != HAL_OK)
      Error_Handler();
}

/* GPIO INIT ------------------------------------------------------------------*/
static void MX_GPIO_Init(void)
{
  GPIO_InitTypeDef GPIO_InitStruct = {0};

  /* Enable all GPIO clocks first */
  __HAL_RCC_GPIOA_CLK_ENABLE();
  __HAL_RCC_GPIOB_CLK_ENABLE();
  __HAL_RCC_GPIOC_CLK_ENABLE();

  /* Initialize LED pins on GPIOB (PB0-PB7) */
  HAL_GPIO_WritePin(GPIOB, LED_PINS, GPIO_PIN_RESET);

  GPIO_InitStruct.Pin = LED_PINS;
  GPIO_InitStruct.Mode = GPIO_MODE_OUTPUT_PP;
  GPIO_InitStruct.Pull = GPIO_NOPULL;
  GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_LOW;
  HAL_GPIO_Init(GPIOB, &GPIO_InitStruct);

  /* NOTE: LCD GPIO initialization is done in init_LCD() function
   * LCD uses: PA12, PA15 (D6, D7)
   *           PB8, PB9 (D4, D5)
   *           PC14, PC15 (RS, EN)
   */
}

/* USART1 INIT ---------------------------------------------------------------*/
static void MX_USART1_UART_Init(void)
{
  huart1.Instance = USART1;
  huart1.Init.BaudRate = 115200;
  huart1.Init.WordLength = UART_WORDLENGTH_8B;
  huart1.Init.StopBits = UART_STOPBITS_1;
  huart1.Init.Parity = UART_PARITY_NONE;
  huart1.Init.Mode = UART_MODE_TX_RX;
  huart1.Init.HwFlowCtl = UART_HWCONTROL_NONE;
  huart1.Init.OverSampling = UART_OVERSAMPLING_16;
  if (HAL_UART_Init(&huart1) != HAL_OK)
      Error_Handler();
}

/* UART RX CALLBACK -----------------------------------------------------------*/
void HAL_UART_RxCpltCallback(UART_HandleTypeDef *huart)
{
    if (huart->Instance == USART1) {
        if (byte == '\r' || byte == '\n') {
            if (rx_index > 0) {
                rx_buffer[rx_index] = '\0';
                cmd_ready = 1;
                rx_index = 0;
            }
        } else if (rx_index < RX_BUFFER_SIZE - 1) {
            rx_buffer[rx_index++] = byte;
        } else {
            // Buffer full
            rx_index = 0;
        }
        HAL_UART_Receive_IT(&huart1, &byte, 1);
    }
}

/* UART SEND FUNCTION ---------------------------------------------------------*/
void send_message(const char *msg)
{
    char temp[80];
    int len = snprintf(temp, sizeof(temp), "%s\n", msg);
    if (len > 0 && len < sizeof(temp)) {
        HAL_UART_Transmit(&huart1, (uint8_t *)temp, len, HAL_MAX_DELAY);
    }
}

/* COMMAND HANDLER ------------------------------------------------------------*/
void process_command(const char *cmd)
{
    lcd_command(CLEAR);
    last_cmd_time = HAL_GetTick();

    if (strcmp(cmd, "CONNECT") == 0) {
        send_message("OK");
        lcd_putstring("Connected");
        lcd_command(LINE_TWO);
        lcd_putstring("UART OK");
        led_mode = LED_MODE_ALL_ON;
        idle_led_mode = LED_MODE_BLINK_ALL;
        HAL_Delay(1000);
        led_mode = idle_led_mode;
    }
    else if (strncmp(cmd, "GET_CODE_", 9) == 0) {
        int i = cmd[9] - '1';
        if (i >= 0 && i < 3) {
            char msg[50];
            snprintf(msg, sizeof(msg), "CODE_%d:%s", i + 1, access_code[i]);
            send_message(msg);
            lcd_putstring("GET CODE");
            lcd_command(LINE_TWO);
            char display[17];
            snprintf(display, sizeof(display), "Slot %d: %.10s", i + 1,
                     access_code[i][0] ? access_code[i] : "Empty");
            lcd_putstring(display);
            single_led = i + 1;
            led_mode = LED_MODE_SINGLE;
        } else {
            send_message("ERR:INVALID_SLOT");
            lcd_putstring("ERROR");
            lcd_command(LINE_TWO);
            lcd_putstring("Invalid Slot");
        }
    }
    else if (strncmp(cmd, "SET_CODE_", 9) == 0) {
        int i = cmd[9] - '1';
        const char *value = strchr(cmd, ':');
        if (i >= 0 && i < 3 && value != NULL) {
            value++;
            strncpy(access_code[i], value, MAX_CODE_LENGTH);
            access_code[i][MAX_CODE_LENGTH] = '\0';
            send_message("SAVED");
            lcd_putstring("SET CODE");
            lcd_command(LINE_TWO);
            char display[17];
            snprintf(display, sizeof(display), "Slot %d Saved", i + 1);
            lcd_putstring(display);
            single_led = i;
            led_mode = LED_MODE_SINGLE;
        } else {
            send_message("ERR:INVALID_FORMAT");
            lcd_putstring("ERROR");
            lcd_command(LINE_TWO);
            lcd_putstring("Bad Format");
        }
    }
    else if (strcmp(cmd, "DISCONNECT") == 0) {
        send_message("BYE");
        lcd_putstring("Disconnected");
        lcd_command(LINE_TWO);
        lcd_putstring("Bye");
        leds_all_on();
        HAL_Delay(1000);
        leds_all_off();
        led_mode = LED_MODE_NONE;
        idle_led_mode = LED_MODE_NONE;
    }
    else if (strcmp(cmd, "STATUS") == 0) {
        char msg[80];
        int stored = 0;
        for (int i = 0; i < 3; i++) {
            if (access_code[i][0] != '\0') stored++;
        }
        snprintf(msg, sizeof(msg), "STATUS:OK,CODES:%d/3", stored);
        send_message(msg);
        lcd_putstring("Status Check");
        lcd_command(LINE_TWO);
        snprintf(msg, sizeof(msg), "%d codes stored", stored);
        lcd_putstring(msg);
    }
    else {
        send_message("ERR:UNKNOWN_CMD");
        lcd_putstring("CMD ERR");
        lcd_command(LINE_TWO);
        lcd_putstring("Unknown Command");
        led_mode = LED_MODE_BLINK_ODD;
    }
}

/* ERROR HANDLER --------------------------------------------------------------*/
void Error_Handler(void)
{
  __disable_irq();
  while (1) {}
}
