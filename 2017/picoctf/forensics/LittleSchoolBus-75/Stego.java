import java.io.*;

public class Stego
{  public static void main(String[] args)
   {  new Stego(); }

   public Stego()
   {  
      decrypt(45);

      System.out.println();
   }  
        
   public void decrypt(int max)
   {      
      try
      {
         RandomAccessFile data = new RandomAccessFile("littleschoolbus.bmp","rw");
         long size = data.length();

         int num = 0;       // adds up the values of the LSB bits
         int power = 128;   // powers of 2 for bit values
         int bits = 0;      // counts bits, stop at 8
         int count = 0;     // counts characters, stopping at max
         
         for (int x=54; x < size; x++)
         {
            data.seek(x);
            byte b = data.readByte();

            b = (byte)(b & 1);         // mask the LSB bit
            
            num = num + b * power;     // add up bit values
            
            bits = bits + 1;           // counting bits up to 8
            
            power = power / 2;         // next power of 2
            
            if (bits % 8 == 0 )        // at end of each byte
            {  char c = (char)num;        // CAST to char
               System.out.print(c);     // print the char
               power = 128;               // start over for next byte
               num = 0;                   // restart total for next byte
               count = count + 1;         // counting chars
               if (count >= max)
               {  return;  }              // stop when max chars printed
            }   
         }
         data.close();
      }
      catch (IOException ex)
      { }
   }
}