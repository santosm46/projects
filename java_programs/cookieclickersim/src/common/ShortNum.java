package common;

public class ShortNum {

//	private static String[] suffix = new String[]{"k", "million", "billion", "trillion", "quadrillion", "quintillion", "sextillion", "septillion", "octillion", "nonetillion", "decatillion"};
	private static String[] suffix = new String[]{"k", "mi", "bi", "tri", "quad", "quin"}; // , "sext", "sept", "octi", "non", "dec"};
	private static int suffixLength = suffix.length;
	
	public static String format(long number) {
		if(number < 1000000 || number >= 1000000000000000000L) {
			return Long.toString(number);
		}
	    return mount(number, suffixLength, longPow(suffixLength));
	}
	
	private static String mount(long number, int suffixPosition, long divider) {
		double shortForm = (double) number / (double)divider;
		
		if(Math.floor(shortForm) == 0) {
			return mount(number, suffixPosition-1, divider / 1000);
		}
		else {
			return String.format("%.3f", shortForm) + " " + suffix[suffixPosition-1];
		}
		
	}
	
	private static long longPow(int power) {
		long base = 1000;
		long result = 1;
		for (int i = 0; i < power; i++) {
			result *= base;
		}
		return result;
	}
	
	public static void test() {
		System.out.println(ShortNum.format(1000000L) + " = 1 mi");
    	System.out.println(ShortNum.format(1237770L) + "1,238 mi");
    	System.out.println(ShortNum.format(1237700000L) + "1,237 bi");
    	System.out.println(ShortNum.format(123700000000L) + "123,7 bi");
    	System.out.println(ShortNum.format(123000000670000L) + "123 tri");
    	System.out.println(ShortNum.format(123020000000500000L) + "123,02 quad");
    	System.out.println(ShortNum.format(1230200000005000000L) + "1230200000005000000L");
	}
}
