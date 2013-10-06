import java.io.File;
import java.io.FileReader;
import java.io.PrintWriter;
import java.util.HashMap;

import au.com.bytecode.opencsv.CSVReader;
import au.com.bytecode.opencsv.CSVWriter;


public class ReadAndDumpCSV {
	public void readAndDumpCsvFile(String inputFileName, String dumpFileName, String wordFreqFileName, int columnNumber) throws Exception{
		CSVReader in = new CSVReader(new FileReader(new File(inputFileName)));
		PrintWriter out = new PrintWriter(new File(dumpFileName)); 
		CSVWriter outCsv = new CSVWriter(new PrintWriter(wordFreqFileName));
		HashMap<String, Integer> freqCount = new HashMap<String, Integer>();
		String line[];
		String lineTokens[];
		in.readNext();
		while( (line = in.readNext()) != null){
			lineTokens = line[columnNumber].split("[\\s\\,\\.\\-\\\\/]");
			out.println(line[columnNumber]);
			for(String word: lineTokens){
				word = cleanWord(word);
				if(word== null)continue;
				if(!freqCount.containsKey(word))
					freqCount.put(word, 1);
				freqCount.put(word, freqCount.get(word)+1);
			}
		}
		for(String key: freqCount.keySet())
			outCsv.writeNext(new String[]{key, freqCount.get(key).toString()});
		in.close();
		out.close();
		outCsv.close();
	}
	private String cleanWord(String word) {
		StringBuilder wordObj = new StringBuilder(word.toLowerCase());
		int i = 0;
		while(i < wordObj.length() && wordObj.length() > 0 && (wordObj.charAt(i) <'a' || wordObj.charAt(i) > 'z') )
			wordObj.deleteCharAt(i++);
		i = wordObj.length()-1;
		while(i >= 0 && wordObj.length() > 0 && (wordObj.charAt(i) <'a' || wordObj.charAt(i) > 'z'))
			wordObj.deleteCharAt(i--);
		if(wordObj.length() <= 0)
			return null;
		return wordObj.toString();
	}
	public static void main(String args[]) throws Exception{
		ReadAndDumpCSV obj = new ReadAndDumpCSV();
		obj.readAndDumpCsvFile("./res/train.csv", "./res/dumped.txt", "./res/wordFreq.csv", 4);
	}
}
