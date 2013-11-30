import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.PrintWriter;
import java.util.Arrays;

import org.joda.time.Days;
import org.joda.time.LocalDateTime;
import org.joda.time.format.DateTimeFormat;
import org.joda.time.format.DateTimeFormatter;

import au.com.bytecode.opencsv.CSVWriter;


public class DumpDays {
	
	public static void main(String[] args) throws Exception{
		//term frequency in the description tag
		//term frequency in the Document as a whole
		new DumpDays().readAndDumpCsvFile("./res/test.csv", "./res/days_feature_test.csv", 9);
		
	}
	public void readAndDumpCsvFile(String inputFileName, String dumpFileName, int columnNumber) throws Exception{
		BufferedReader in = new BufferedReader(new FileReader(new File(inputFileName)));
		CSVWriter outCsv = new CSVWriter(new PrintWriter(dumpFileName));
		String line[];
		String lineString;
		int id = 1;
		DateTimeFormatter dateTimeFormatter = DateTimeFormat.forPattern("yyyy-MM-dd HH:mm:ss");
		LocalDateTime endDateTime = DateTimeFormat.forPattern("yyyy-MM-dd").parseLocalDateTime("2013-09-17"); 
		in.readLine();
		while( (lineString = in.readLine()) != null ){
			line = lineString.split("(\",\")");
			LocalDateTime currentDateTime = null;
			try {
				currentDateTime = dateTimeFormatter.parseLocalDateTime(line[columnNumber].trim());
			} catch (Exception e1) {
				try {
					currentDateTime = dateTimeFormatter.parseLocalDateTime(line[line.length-2].trim());
				} catch (Exception e2) {
					System.out.println("Error at line: ");
					System.out.println("line " + id + "\n" + Arrays.toString(line));
				}
			}
			Days diff = null;
			try {
				diff  = Days.daysBetween(endDateTime, currentDateTime);
				outCsv.writeNext( new String[]{String.valueOf(id), String.valueOf( 1.0/(1+Math.log10(1+-1*diff.getDays())))  } );
			} catch (Exception e) {
				System.out.println("\n*\n*\n*\n*\nCheck line " + id  + "\n" + line.length + "\n" + Arrays.toString(line));
				System.out.println("Cell data: " + line[columnNumber]);
			}
			id++;
		}
		in.close();
		outCsv.close();
	}	


}
