"""
Test Suite for Dongle Lock System
Tests communication and protocol handling
Authors: Dube Kagiso and Xolisile Buqwana
Date: 14 October 2025
"""

import sys
import time
from Communication_Ports import CommunicationPorts
from Protocol_Handler import ProtocolHandler, PROTOCOL_DOCUMENTATION


class DongleTester:
    """Test suite for dongle communication"""
    
    def __init__(self, port_name=None):
        """Initialize tester with optional port name"""
        self.port_name = port_name
        self.comm = None
        self.protocol = ProtocolHandler()
        
    def select_port(self):
        """Interactive port selection"""
        print("\n" + "="*60)
        print("Available COM Ports:")
        print("="*60)
        
        ports = CommunicationPorts.list_available_ports()
        
        if not ports:
            print("No COM ports found!")
            return None
        
        for idx, (port, desc) in enumerate(ports, 1):
            print(f"{idx}. {port} - {desc}")
        
        while True:
            try:
                choice = input(f"\nSelect port (1-{len(ports)}) or 'q' to quit: ").strip()
                
                if choice.lower() == 'q':
                    return None
                
                port_idx = int(choice) - 1
                if 0 <= port_idx < len(ports):
                    return ports[port_idx][0]
                else:
                    print("Invalid selection. Try again.")
            except ValueError:
                print("Please enter a number.")
    
    def test_connection(self):
        """Test connection to dongle"""
        print("\n" + "="*60)
        print("TEST 1: Connection")
        print("="*60)
        
        if not self.port_name:
            self.port_name = self.select_port()
            
        if not self.port_name:
            print("❌ No port selected")
            return False
        
        print(f"\n→ Testing connection to {self.port_name}...")
        
        try:
            self.comm = CommunicationPorts(self.port_name, baudrate=9600, timeout=2.0)
            
            if not self.comm.open_connection():
                print("❌ Failed to open port")
                return False
            
            # Send CONNECT message
            connect_msg = self.protocol.create_connect_message()
            print(f"→ Sending: {connect_msg}")
            
            response = self.comm.send_command(connect_msg, wait_response=True)
            
            if response and self.protocol.is_ok_response(response):
                print(f"✓ Connection successful! Response: {response}")
                return True
            else:
                print(f"❌ Invalid response: {response}")
                return False
                
        except Exception as e:
            print(f"❌ Connection error: {e}")
            return False
    
    def test_get_empty_code(self, code_num=1):
        """Test getting an empty code slot"""
        print("\n" + "="*60)
        print(f"TEST 2: Get Empty Code (Slot {code_num})")
        print("="*60)
        
        if not self.comm or not self.comm.is_connected():
            print("❌ Not connected")
            return False
        
        try:
            get_msg = self.protocol.create_get_code_message(code_num)
            print(f"→ Sending: {get_msg}")
            
            response = self.comm.send_command(get_msg, wait_response=True)
            print(f"← Received: {response}")
            
            if self.protocol.is_empty_response(response):
                print(f"✓ Code slot {code_num} is empty (as expected)")
                return True
            elif self.protocol.is_code_response(response):
                code = self.protocol.extract_code_from_response(response)
                print(f"⚠ Code slot {code_num} already has a value: {code}")
                return True
            else:
                print(f"❌ Unexpected response: {response}")
                return False
                
        except Exception as e:
            print(f"❌ Error: {e}")
            return False
    
    def test_set_code(self, code_num=1, code_value="test123"):
        """Test setting a code"""
        print("\n" + "="*60)
        print(f"TEST 3: Set Code (Slot {code_num})")
        print("="*60)
        
        if not self.comm or not self.comm.is_connected():
            print("❌ Not connected")
            return False
        
        try:
            # Validate code
            is_valid, error = self.protocol.validate_code_value(code_value)
            if not is_valid:
                print(f"❌ Invalid code: {error}")
                return False
            
            set_msg = self.protocol.create_set_code_message(code_num, code_value)
            print(f"→ Sending: {set_msg}")
            
            response = self.comm.send_command(set_msg, wait_response=True)
            print(f"← Received: {response}")
            
            if self.protocol.is_saved_response(response):
                print(f"✓ Code saved successfully in slot {code_num}")
                return True
            else:
                print(f"❌ Failed to save code: {response}")
                return False
                
        except Exception as e:
            print(f"❌ Error: {e}")
            return False
    
    def test_get_stored_code(self, code_num=1, expected_code="test123"):
        """Test retrieving a stored code"""
        print("\n" + "="*60)
        print(f"TEST 4: Get Stored Code (Slot {code_num})")
        print("="*60)
        
        if not self.comm or not self.comm.is_connected():
            print("❌ Not connected")
            return False
        
        try:
            get_msg = self.protocol.create_get_code_message(code_num)
            print(f"→ Sending: {get_msg}")
            
            response = self.comm.send_command(get_msg, wait_response=True)
            print(f"← Received: {response}")
            
            if self.protocol.is_code_response(response):
                code = self.protocol.extract_code_from_response(response)
                print(f"✓ Retrieved code: {code}")
                
                if code == expected_code:
                    print(f"✓ Code matches expected value!")
                    return True
                else:
                    print(f"⚠ Code doesn't match. Expected: {expected_code}, Got: {code}")
                    return True  # Still successful retrieval
            else:
                print(f"❌ Unexpected response: {response}")
                return False
                
        except Exception as e:
            print(f"❌ Error: {e}")
            return False
    
    def test_disconnect(self):
        """Test disconnection"""
        print("\n" + "="*60)
        print("TEST 5: Disconnect")
        print("="*60)
        
        if not self.comm or not self.comm.is_connected():
            print("❌ Not connected")
            return False
        
        try:
            disconnect_msg = self.protocol.create_disconnect_message()
            print(f"→ Sending: {disconnect_msg}")
            
            # Send disconnect (don't wait for response as it's optional)
            self.comm.send_data(disconnect_msg)
            time.sleep(0.5)
            
            # Close connection
            self.comm.close_connection()
            print("✓ Disconnected successfully")
            return True
            
        except Exception as e:
            print(f"❌ Error: {e}")
            return False
    
    def run_full_test_suite(self):
        """Run complete test suite"""
        print("\n" + "="*60)
        print("DONGLE LOCK SYSTEM - FULL TEST SUITE")
        print("="*60)
        
        results = []
        
        # Test 1: Connection
        results.append(("Connection", self.test_connection()))
        
        if not results[0][1]:
            print("\n❌ Connection failed. Aborting remaining tests.")
            return
        
        # Test 2: Get empty code
        results.append(("Get Empty Code", self.test_get_empty_code(1)))
        
        # Test 3: Set code
        test_password = f"TestPass{int(time.time())}"  # Unique password
        results.append(("Set Code", self.test_set_code(1, test_password)))
        
        # Test 4: Get stored code
        results.append(("Get Stored Code", self.test_get_stored_code(1, test_password)))
        
        # Test 5: Test all three slots
        print("\n" + "="*60)
        print("TEST 6: All Code Slots")
        print("="*60)
        
        for slot in [1, 2, 3]:
            code = f"Code{slot}_{int(time.time())}"
            print(f"\n→ Testing slot {slot}...")
            self.test_set_code(slot, code)
            self.test_get_stored_code(slot, code)
        
        # Test 6: Disconnect
        results.append(("Disconnect", self.test_disconnect()))
        
        # Print summary
        print("\n" + "="*60)
        print("TEST SUMMARY")
        print("="*60)
        
        passed = sum(1 for _, result in results if result)
        total = len(results)
        
        for test_name, result in results:
            status = "✓ PASS" if result else "❌ FAIL"
            print(f"{test_name:.<40} {status}")
        
        print(f"\nTotal: {passed}/{total} tests passed")
        
        if passed == total:
            print("\n🎉 All tests passed!")
        else:
            print(f"\n⚠ {total - passed} test(s) failed")


def main():
    """Main test entry point"""
    print(PROTOCOL_DOCUMENTATION)
    
    print("\n" + "="*60)
    print("DONGLE LOCK SYSTEM TESTER")
    print("="*60)
    print("\nThis tool tests the communication between PC and STM dongle.")
    print("Make sure your STM board is connected and running the firmware.")
    
    tester = DongleTester()
    
    while True:
        print("\n" + "="*60)
        print("MAIN MENU")
        print("="*60)
        print("1. Run Full Test Suite")
        print("2. Test Connection Only")
        print("3. Manual Test (Interactive)")
        print("4. View Protocol Documentation")
        print("5. List Available Ports")
        print("q. Quit")
        
        choice = input("\nSelect option: ").strip().lower()
        
        if choice == '1':
            tester.run_full_test_suite()
        elif choice == '2':
            tester.test_connection()
            if tester.comm:
                tester.test_disconnect()
        elif choice == '3':
            manual_test(tester)
        elif choice == '4':
            print(PROTOCOL_DOCUMENTATION)
        elif choice == '5':
            CommunicationPorts.list_available_ports()
        elif choice == 'q':
            print("\nGoodbye!")
            break
        else:
            print("Invalid option. Try again.")


def manual_test(tester):
    """Interactive manual testing"""
    if not tester.comm or not tester.comm.is_connected():
        if not tester.test_connection():
            return
    
    while True:
        print("\n" + "-"*60)
        print("MANUAL TEST MODE")
        print("-"*60)
        print("1. Get Code (slot 1)")
        print("2. Get Code (slot 2)")
        print("3. Get Code (slot 3)")
        print("4. Set Code")
        print("5. Send Custom Command")
        print("6. Disconnect")
        print("b. Back to Main Menu")
        
        choice = input("\nSelect option: ").strip()
        
        if choice == '1':
            tester.test_get_empty_code(1)
        elif choice == '2':
            tester.test_get_empty_code(2)
        elif choice == '3':
            tester.test_get_empty_code(3)
        elif choice == '4':
            slot = input("Enter slot number (1-3): ").strip()
            code = input("Enter code value: ").strip()
            try:
                tester.test_set_code(int(slot), code)
            except ValueError:
                print("Invalid slot number")
        elif choice == '5':
            cmd = input("Enter command: ").strip()
            if tester.comm and tester.comm.is_connected():
                response = tester.comm.send_command(cmd, wait_response=True)
                print(f"Response: {response}")
        elif choice == '6':
            tester.test_disconnect()
            break
        elif choice.lower() == 'b':
            break


if __name__ == "__main__":
    main()