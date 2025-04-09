#include "MSP430IO.H"
#define testPIN S1

void setup() {
  pinMode(E1, OUTPUT);
  pinMode(E2, OUTPUT);
  pinMode(E3, OUTPUT);
  pinMode(A, OUTPUT);
  pinMode(B, OUTPUT);
  pinMode(C, OUTPUT);
  pinMode(S0, OUTPUT);
  pinMode(S1, OUTPUT);
  pinMode(S2, OUTPUT);
  pinMode(Master_C, OUTPUT);
  pinMode(Sel_OR, OUTPUT);
  pinMode(Data_IN , OUTPUT);


  // Wait for the software reset to occur
 // while (255);
unsigned char WriteByte = 0xFF; // Initialize byte to 0xFF (all bits set to 1)

  WriteByte = 0x00; // Clear byte to 0 (all bits set to 0)
	
}
void WriteByte (int IC, int Y, int VAL ) {
  for (int S = 0; S <= 7; S++) {
    sel(S);
    digitalWrite(Data_IN, bitRead(VAL, S));
    en(IC);
    adr(Y);
    clockEnable();
    //delay(250);
  }
}
void clockEnable() {
  digitalWrite(Sel_OR, HIGH);
  digitalWrite(Sel_OR, LOW);
}
void sel (int num) {
  // for( int num = 0; num <= 7; num ++){
  digitalWrite(S0, bitRead(num, 0));
  digitalWrite(S1, bitRead(num, 1));
  digitalWrite(S2, bitRead(num, 2));
  //delay(500);
  //}
}
void en (int num) {
  // for( int num = 0; num <= 7; num ++){
  digitalWrite(E1, bitRead(num, 0));
  digitalWrite(E2, bitRead(num, 1));
  digitalWrite(E3, bitRead(num, 2));
  //delay(500);
  //}
}
void adr (int num) {
  // for( int num = 0; num <= 7; num ++){
  digitalWrite(A, bitRead(num, 0));
  digitalWrite(B, bitRead(num, 1));
  digitalWrite(C, bitRead(num, 2));
  //delay(500);
  //}
}
/* mode 0
    mode 1 is demultiplex
    mode 2
    mode 3 is memory
*/
void loop() {
  //flashPIN();
  //en(4);
  //adr(0);
  // sel(5);
  // mode(3);
  // digitalWrite(Data_IN_LOW);
 // for (int count = 0; count <= 7; count ++) {
    WriteByte (4, 0, 255);
    delay(250);
  }
//}
