package theGUI;

import java.awt.BorderLayout;
import java.awt.Color;
import java.awt.FlowLayout;
import java.awt.GridLayout;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.util.ArrayList;
import java.util.Observable;
import java.util.Observer;

import javax.swing.JButton;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JOptionPane;
import javax.swing.JPanel;
import javax.swing.JSlider;
import javax.swing.JTextField;

 /**
 * The GUI's view and control class which interacts with the Observable model
 * to produce the solver interface
 * 
 * @author Michael C Albert 
 */	

public class EdibleViewControl extends JFrame implements Observer {
	
	/**
	 * 
	 */
	private static final long serialVersionUID = 2707336261155259187L;

	/**
	 * The model
	 */
	private static Communicator model;
	
	/**
	 * The suggestion
	 */
	private String chefBotSays;
	
	/**
	 * The current interface
	 */
	private boolean mainUI;
	
	/**
	 * The information to be displayed
	 */
	private JLabel info;
	
	/**
	 * The label for the slider
	 */
	private JLabel sliderLabel;
	
	/**
	 * The label for the size
	 */
	private JLabel sizeLabel;
	
	/**
	 * The label for the query
	 */
	private JLabel queryLabel;
	
	/**
	 * The recipe quality slider
	 */
	private JSlider quality;
	
	/**
	 * The recipe size slider
	 */
	private JSlider size;
	
	/**
	 * The UI for inputs
	 */
	private JPanel topPanel;
	
	/**
	 * The top info
	 */
	private JPanel topInfo;
	
	/**
	 * The UI for chefBot solution
	 */
	private JPanel chefPanel;
	
	/**
	 * The UI for chefBot solution
	 */
	private JLabel chefLabel;
	
	/**
	 * The color list
	 */
	private ArrayList<Color> colors;
	
	/**
	 * The action button
	 */
	private JButton send;

	/**
	 * The text input
	 */
	public static JTextField textInput;
	
	
	/**
	 * Constructor for edible user interface
	 * 
	 * @param eModel
	 * the model to be used by the EdibleViewControl
	 * 
	 */	
	public EdibleViewControl(Communicator eModel){
		
        setDefaultLookAndFeelDecorated(true);
		
        mainUI = true;
		model = eModel;
		info = new JLabel();
		info.setFont(info.getFont().deriveFont(20.0f));
		sliderLabel = new JLabel("Recipe Variety");
		sizeLabel = new JLabel("Size of Recipe");
		queryLabel = new JLabel("Enter edible query");
		chefLabel = new JLabel(chefBotSays);
		colors = new ArrayList<Color>();
		textInput = new JTextField("");
		quality = new JSlider(JSlider.HORIZONTAL,0,100,50);
		quality.setBackground(Color.WHITE);
		size = new JSlider(JSlider.HORIZONTAL,0,15,5);
		size.setBackground(Color.WHITE);
		topPanel = new JPanel();
		topPanel.setLayout(new BorderLayout());
		chefPanel = new JPanel();
		chefPanel.setLayout(new BorderLayout());
		
		colors.add(Color.BLACK);
		colors.add(Color.WHITE);
		setBackground(Color.WHITE);
		
		setTitle("edible");
		
		setLayout(new BorderLayout());
		setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);
		ButtonListener solveIt = new ButtonListener();
		
		JPanel theQuery = new JPanel();
    	theQuery.setLayout(new GridLayout(1,2));
    	theQuery.setBackground(Color.WHITE);
		
		JPanel theQuality = new JPanel();
    	theQuality.setLayout(new GridLayout(1,2));
    	theQuality.setBackground(Color.WHITE);
    	
    	JPanel theSize = new JPanel();
    	theSize.setLayout(new GridLayout(1,2));
    	theSize.setBackground(Color.WHITE);
		
    	topInfo = new JPanel();
    	topInfo.setLayout(new FlowLayout(FlowLayout.CENTER));
    	topInfo.setBackground(Color.WHITE);
    	
    	JPanel inputs = new JPanel();
    	inputs.setLayout(new GridLayout(3,1));
    	/*JPanel inputArea = new JPanel();
    	inputArea.setLayout(new FlowLayout(FlowLayout.LEFT));*/
    	
		send = new JButton("Give to chefBot");
    	send.addActionListener(solveIt);
    	send.setVisible(true);
    	
    	JButton back = new JButton("Return");
    	back.addActionListener(solveIt);
    	back.setVisible(true);
		
    	chefLabel.setBackground(Color.WHITE);
    	chefPanel.setBackground(Color.WHITE);
    	
    	info.setText("<html>chefBot is <font color='red'>watching</font></html>");
    	info.setVisible(true);
    	sliderLabel.setVisible(true);
    	sizeLabel.setVisible(true);
    	queryLabel.setVisible(true);
    	quality.setVisible(true);
    	size.setVisible(true);
    	chefLabel.setVisible(true);
    	
    	
    	/*textInput.setBackground(Color.BLUE);
    	textInput.setForeground(Color.WHITE);*/
    	
    	topInfo.add(info);
    	
    	theQuery.add(queryLabel);
    	theQuery.add(textInput);
    	theQuality.add(sliderLabel);
    	theQuality.add(quality);
    	theSize.add(sizeLabel);
    	theSize.add(size);
    	
    	inputs.add(theQuery);
    	inputs.add(theQuality);
    	inputs.add(theSize);

    	topPanel.add(send, BorderLayout.SOUTH);
    	topPanel.add(inputs, BorderLayout.CENTER);
    	/*topPanel.add(topInfo, BorderLayout.NORTH);*/
    	
    	chefPanel.add(back, BorderLayout.SOUTH);
    	/*chefPanel.add(topInfo, BorderLayout.NORTH);*/
    	chefPanel.add(chefLabel, BorderLayout.CENTER);
    	
    	/*bButtons.add(send, BorderLayout.CENTER);*/
    	
		/*add(inputArea, BorderLayout.CENTER);
		add(send, BorderLayout.SOUTH);
		add(inputs, BorderLayout.CENTER);
		add(topInfo, BorderLayout.NORTH);
		*/
    	
    	add(topInfo, BorderLayout.NORTH);
    	add(topPanel, BorderLayout.CENTER);
		setVisible(true);
		setSize(400, 200);
		setLocation(100,100);
		
		pack();
		setResizable(false);
		
}
	
	
    class ButtonListener implements ActionListener {

    	/**
    	 * Performs the necessary procedures when the GUI's buttons are triggered
    	 * 
    	 * @param event
    	 * 		the ActionEvent object which triggered the event
    	 * 
    	 */	
        public void actionPerformed(ActionEvent event) {
        
        	if(mainUI){
	        	String theText = textInput.getText();
	        	
	        	Integer theQuality = 100 - quality.getValue();
	        	Integer theSize = size.getValue();
	        	textInput.setText("");
	        	
	        	if(theText.equals("")){
	        		JOptionPane.showMessageDialog(null, "Cannot enter nothing!");
	        		return;
	        	}
	        	
	        	theText = theQuality.toString()+"|"+theSize.toString()+"|"+theText;
	        	
	        	setChefPanel();
	        	
	        	model.sendQuery(theText);
	        	model.pipeOut();
	        	
        	}
        	else{
        		setTopPanel();
        		model.returned();
        	
        	}
        	
        }
        
    }

    private void setTopPanel(){
    	getLayout().removeLayoutComponent(chefPanel);
    	chefPanel.setVisible(false);
    	topPanel.setVisible(true);
    	add(topPanel, BorderLayout.CENTER);
		mainUI = true;
    }
    
    private void setChefPanel(){
    	getLayout().removeLayoutComponent(topPanel);
    	topPanel.setVisible(false);
    	chefPanel.setVisible(true);
    	add(chefPanel, BorderLayout.CENTER);
		mainUI = false;
    }
    
	@Override
	public void update(Observable o, Object arg) {
		if(mainUI){
			info.setText("<html>chefBot is <font color='red'>watching</font></html>");
			pack();
		}
		else{
			info.setText("<html>chefBot is <font color='green'>suggesting</font></html>");
			setResizable(true);
			chefBotSays = model.getText();
			chefLabel.setText(chefBotSays);
			pack();
			setResizable(false);
			/*JOptionPane.showMessageDialog(null, chefBotSays);*/
		}
	}
    
}
