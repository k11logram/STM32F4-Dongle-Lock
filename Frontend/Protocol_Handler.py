"""
Protocol Handler Module
Defines the message protocol for STM Dongle communication
Authors: Dube Kagiso and Xolisile Buqwana
Date: 14 October 2025
"""

from enum import Enum
from typing import Optional, Tuple
from dataclasses import dataclass


class MessageType(Enum):
    """Enumeration of message types in the protocol"""
    CONNECT = "CONNECT"
    DISCONNECT = "DISCONNECT"
    GET_CODE_1 = "GET_CODE_1"
    GET_CODE_2 = "GET_CODE_2"
    GET_CODE_3 = "GET_CODE_3"
    SET_CODE_1 = "SET_CODE_1"
    SET_CODE_2 = "SET_CODE_2"
    SET_CODE_3 = "SET_CODE_3"
    
    # Response types
    OK = "OK"
    EMPTY = "EMPTY"
    CODE = "CODE"
    SAVED = "SAVED"
    BYE = "BYE"
    ERROR = "ERROR"


@dataclass
class Message:
    """Represents a protocol message"""
    msg_type: str
    payload: Optional[str] = None
    
    def to_string(self) -> str:
        """Convert message to protocol string format"""
        if self.payload:
            return f"{self.msg_type}:{self.payload}"
        return self.msg_type
    
    @classmethod
    def from_string(cls, msg_string: str) -> 'Message':
        """Parse a protocol string into a Message object"""
        if ':' in msg_string:
            msg_type, payload = msg_string.split(':', 1)
            return cls(msg_type=msg_type.strip(), payload=payload.strip())
        return cls(msg_type=msg_string.strip())


class ProtocolHandler:
    """Handles protocol message creation and parsing"""
    
    @staticmethod
    def create_connect_message() -> str:
        """Create CONNECT message"""
        return MessageType.CONNECT.value
    
    @staticmethod
    def create_disconnect_message() -> str:
        """Create DISCONNECT message"""
        return MessageType.DISCONNECT.value
    
    @staticmethod
    def create_get_code_message(code_num: int) -> str:
        """
        Create GET_CODE_N message
        
        Args:
            code_num: Code number (1, 2, or 3)
            
        Returns:
            str: GET_CODE message
        """
        if code_num not in [1, 2, 3]:
            raise ValueError("Code number must be 1, 2, or 3")
        return f"GET_CODE_{code_num}"
    
    @staticmethod
    def create_set_code_message(code_num: int, code_value: str) -> str:
        """
        Create SET_CODE_N:value message
        
        Args:
            code_num: Code number (1, 2, or 3)
            code_value: The access code to store
            
        Returns:
            str: SET_CODE message with payload
        """
        if code_num not in [1, 2, 3]:
            raise ValueError("Code number must be 1, 2, or 3")
        if not code_value:
            raise ValueError("Code value cannot be empty")
        return f"SET_CODE_{code_num}:{code_value}"
    
    @staticmethod
    def parse_response(response: str) -> Message:
        """
        Parse a response message from the STM
        
        Args:
            response: Raw response string
            
        Returns:
            Message: Parsed message object
        """
        return Message.from_string(response)
    
    @staticmethod
    def is_ok_response(response: str) -> bool:
        """Check if response is OK"""
        return response.strip() == MessageType.OK.value
    
    @staticmethod
    def is_empty_response(response: str) -> bool:
        """Check if response indicates empty code slot"""
        return response.strip() == MessageType.EMPTY.value
    
    @staticmethod
    def is_saved_response(response: str) -> bool:
        """Check if response indicates successful save"""
        return response.strip() == MessageType.SAVED.value
    
    @staticmethod
    def is_code_response(response: str) -> bool:
        """Check if response contains a code"""
        return response.strip().startswith(MessageType.CODE.value + ":")
    
    @staticmethod
    def extract_code_from_response(response: str) -> Optional[str]:
        """
        Extract code value from CODE:value response
        
        Args:
            response: Response string
            
        Returns:
            str: Extracted code value or None if invalid format
        """
        if ProtocolHandler.is_code_response(response):
            msg = Message.from_string(response)
            return msg.payload
        return None
    
    @staticmethod
    def validate_code_number(code_num: int) -> bool:
        """Validate that code number is in valid range"""
        return code_num in [1, 2, 3]
    
    @staticmethod
    def validate_code_value(code_value: str) -> Tuple[bool, str]:
        """
        Validate code value meets requirements
        
        Args:
            code_value: The code to validate
            
        Returns:
            Tuple[bool, str]: (is_valid, error_message)
        """
        if not code_value:
            return False, "Code cannot be empty"
        
        if len(code_value) > 50:
            return False, "Code is too long (max 50 characters)"
        
        # Check for invalid characters (newlines, special control chars)
        if '\n' in code_value or '\r' in code_value:
            return False, "Code cannot contain newline characters"
        
        return True, ""


# Protocol documentation
PROTOCOL_DOCUMENTATION = """
=== Dongle Lock Message Protocol ===

1. GUI → STM Messages:
   - CONNECT              : Initiate connection with dongle
   - GET_CODE_1           : Request code from slot 1
   - GET_CODE_2           : Request code from slot 2
   - GET_CODE_3           : Request code from slot 3
   - SET_CODE_1:value     : Store code in slot 1
   - SET_CODE_2:value     : Store code in slot 2
   - SET_CODE_3:value     : Store code in slot 3
   - DISCONNECT           : Close connection with dongle

2. STM to GUI Responses:
   - OK                   : Connection successful
   - CODE:value           : Return stored code value
   - EMPTY                : Code slot is empty
   - SAVED                : Code stored successfully
   - BYE                  : Disconnection acknowledged (optional)
   - ERROR                : Error occurred

3. Message Format:
   - All messages are ASCII text
   - Messages end with newline character (\n)
   - Format: COMMAND or COMMAND:PAYLOAD
   - Maximum message length: 64 characters

4. Communication Flow:
   a) Connection:
      GUI → CONNECT
      STM → OK (if successful)
   
   b) Get Existing Code:
      GUI → GET_CODE_N
      STM → CODE:value (if exists) or EMPTY (if not set)
   
   c) Set New Code:
      GUI → SET_CODE_N:value
      STM → SAVED (if successful)
   
   d) Disconnection:
      GUI → DISCONNECT
      STM → BYE (optional)
"""


# Example usage
if __name__ == "__main__":
    print(PROTOCOL_DOCUMENTATION)
    print("\n=== Protocol Handler Test ===\n")
    
    # Create messages
    print("Creating messages:")
    print(f"CONNECT: {ProtocolHandler.create_connect_message()}")
    print(f"GET_CODE_1: {ProtocolHandler.create_get_code_message(1)}")
    print(f"SET_CODE_2: {ProtocolHandler.create_set_code_message(2, 'myPassword123')}")
    print(f"DISCONNECT: {ProtocolHandler.create_disconnect_message()}")
    print()
    
    # Parse responses
    print("Parsing responses:")
    responses = ["OK", "EMPTY", "CODE:secret123", "SAVED", "ERROR"]
    for resp in responses:
        msg = ProtocolHandler.parse_response(resp)
        print(f"  '{resp}' → Type: {msg.msg_type}, Payload: {msg.payload}")
    print()
    
    # Extract code
    code_response = "CODE:mySecretPassword"
    code = ProtocolHandler.extract_code_from_response(code_response)
    print(f"Extracted code from '{code_response}': {code}")
    print()
    
    # Validate code
    valid, error = ProtocolHandler.validate_code_value("valid_password123")
    print(f"Validate 'valid_password123': {valid}, {error}")
    
    valid, error = ProtocolHandler.validate_code_value("")
    print(f"Validate empty string: {valid}, {error}")
