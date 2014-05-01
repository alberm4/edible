package theGUI;

import java.io.BufferedWriter;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileWriter;
import java.io.IOException;
import java.util.Observable;
import java.util.Scanner;

import javax.swing.UIManager;
import javax.swing.UnsupportedLookAndFeelException;

 /**
 * The communication between the GUI and the edible client
 * @author Michael C Albert 
 */	
public class Communicator extends Observable {
	
	private String theSuggestion;
	
	/**
	 * The associated GUI
	 */
	private final String inFile = "";

	/**
	 * The associated GUI
	 */
	private final String outFile = "";

	/**
	 * The associated GUI
	 */
	private static EdibleViewControl GUI;
	
	public Communicator() {
		
	    try {
        UIManager.setLookAndFeel(
        		UIManager.getCrossPlatformLookAndFeelClassName());
	    } 
	    catch (UnsupportedLookAndFeelException e) {
	       // handle exception
	    	System.out.println("Unsupported");
	    }
	    catch (ClassNotFoundException e) {
	       // handle exception
	    	System.out.println("Not found");
	    }
	    catch (InstantiationException e) {
	       // handle exception
	    	System.out.println("Didn't instantiate");
	    }
	    catch (IllegalAccessException e) {
	       // handle exception
	    	System.out.println("Couldn't access");
	    }
        		
		GUI = new EdibleViewControl(this);
		addObserver(GUI);
	}
	
	public void pipeOut() {
		
		String theText = "";
		String done;
		Boolean go = false;
		
		File theFile = new File(outFile);
		
		Scanner in;
		try {
			while(!go){
				in = new Scanner(theFile);
				if(in.hasNextLine()){ done = in.nextLine(); }
				else{ done = "no"; }
				
				if(done.equals("no")){ go = false;}
				else { go = true; }
				
				if(go){
					theText = done;
					while(in.hasNextLine()){
						theText += in.nextLine();
					}
				}
				
				in.close();
			}
		} catch (FileNotFoundException e) {
			e.printStackTrace();
		}

		theSuggestion = theText;
		try {
			  
			File query = new File(outFile);
 
			FileWriter theWriter = new FileWriter(query.getAbsoluteFile());
			BufferedWriter bufferedWriter = new BufferedWriter(theWriter);
			bufferedWriter.write("");
			
			bufferedWriter.close();

 
		} catch (IOException e) {
			e.printStackTrace();
		}
		
		setChanged();
		notifyObservers();
		
	}

	public void sendQuery(String theText) {
		try {
			  
			File query = new File(inFile);
 
			FileWriter theWriter = new FileWriter(query.getAbsoluteFile());
			BufferedWriter bufferedWriter = new BufferedWriter(theWriter);
			bufferedWriter.write(theText);
			
			bufferedWriter.close();

 
		} catch (IOException e) {
			e.printStackTrace();
		}
		
	}
	
	public void returned(){
		
		saveQuery();
		
		setChanged();
		notifyObservers();
		
	}
	
	private void saveQuery(){
		return;
	}
	
	public String getText() {
		
		return theSuggestion;
		
	}

	public static void main(String[] args) {

		new Communicator();
		
	}

}

