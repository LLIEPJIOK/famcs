import java.awt.Color;
import java.awt.Font;
import java.awt.Insets;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.WindowAdapter;
import java.awt.event.WindowEvent;
import java.io.File;

import javax.swing.BorderFactory;
import javax.swing.JButton;
import javax.swing.JFileChooser;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JScrollPane;
import javax.swing.JTextArea;
import javax.swing.JTextField;
import javax.swing.border.Border;
import javax.swing.border.CompoundBorder;
import javax.swing.border.EmptyBorder;
import javax.swing.border.LineBorder;

public class MainFrame extends JFrame implements ActionListener {
    private static JButton start;
    private static JButton chooseFileButton;

    private static JTextArea log;
    private static JButton stop;

    private static JTextField path_input;

    private ReadThread readThread;
    private WorkingThread workingThread;
    private CheckThread checkThread;

    MainFrame() {
        this.setTitle("RGR2");
        this.setLayout(null);
        this.setLocation(300, 300);
        this.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        this.addWindowListener(new WindowAdapter() {
            @Override
            public void windowClosing(WindowEvent e) {
                try {
                    if (readThread != null && readThread.isAlive()) {
                        readThread.stopThread();
                        readThread.join();
                    }
                    if (workingThread != null && workingThread.isAlive()) {
                        workingThread.stopThread();
                        workingThread.join();
                    }
                    if (checkThread != null && checkThread.isAlive()) {
                        checkThread.stopThread();
                        checkThread.join();
                    }
                } catch (InterruptedException ex) {
                    throw new RuntimeException(ex);
                }
            }
        });

        this.setResizable(false);
        this.setSize(405, 415);
        this.getContentPane().setBackground(new Color(205, 245, 250, 255));
        this.setLocation(100, 100);

        Border roundedBorder = new LineBorder(Color.BLACK, 2, false);
        start = new JButton("Start");
        start.setBounds(250, 30, 90, 35);
        start.addActionListener(this);
        start.setFocusPainted(false);
        start.setBackground(new Color(225, 243, 246, 255));
        start.setForeground(Color.BLACK);
        start.setFont(new Font("Arial", Font.BOLD, 14));
        start.setBorder(new CompoundBorder(roundedBorder, new EmptyBorder(3, 3, 3, 3)));
        start.setHorizontalTextPosition(JButton.CENTER);
        start.setVerticalTextPosition(JButton.CENTER);

        stop = new JButton("Stop");
        stop.addActionListener(this);
        stop.setBounds(250, 70, 125, 35);
        stop.setFocusPainted(false);
        stop.setBackground(new Color(225, 243, 246, 255));
        stop.setForeground(Color.BLACK);
        stop.setFont(new Font("Arial", Font.BOLD, 14));
        stop.setBorder(new CompoundBorder(roundedBorder, new EmptyBorder(3, 3, 3, 3)));
        stop.setHorizontalTextPosition(JButton.CENTER);
        stop.setVerticalTextPosition(JButton.CENTER);
        stop.setEnabled(false);

        chooseFileButton = new JButton("...");
        chooseFileButton.setBounds(345, 30, 30, 35);
        chooseFileButton.addActionListener(this);
        chooseFileButton.setFocusPainted(false);
        chooseFileButton.setBackground(new Color(225, 243, 246, 255));
        chooseFileButton.setForeground(Color.BLACK);
        chooseFileButton.setFont(new Font("Arial", Font.BOLD, 14));
        chooseFileButton.setBorder(new CompoundBorder(roundedBorder, new EmptyBorder(3, 3, 3, 3)));
        chooseFileButton.setHorizontalTextPosition(JButton.CENTER);
        chooseFileButton.setVerticalTextPosition(JButton.CENTER);

        log = new JTextArea();
        log.setMargin(new Insets(10, 10, 10, 10));
        log.setFont(new Font("Arial", Font.BOLD, 14));
        log.setEditable(false);

        JScrollPane scrollPane = new JScrollPane(log);
        scrollPane.setBounds(15, 110, 360, 250);
        scrollPane.setBorder(BorderFactory.createLineBorder(Color.BLACK));

        JLabel logName = new JLabel("Log:");
        logName.setBounds(175, 90, 90, 14);
        logName.setFont(new Font("Arial", Font.BOLD, 14));

        path_input = new JTextField();
        path_input.setBounds(15, 30, 225, 35);
        path_input.setEnabled(false);
        path_input.setDisabledTextColor(Color.BLACK);
        path_input.setBorder(new CompoundBorder(roundedBorder, new EmptyBorder(3, 3, 3, 3)));
        path_input.setFont(new Font("Arial", Font.BOLD, 12));
        path_input.setText("Your directory");
        path_input.setBackground(new Color(225, 243, 246, 255));
        path_input.setEditable(false);

        this.add(start);
        this.add(chooseFileButton);
        this.add(scrollPane);
        this.add(path_input);
        this.add(logName);
        this.add(stop);

    }

    @Override
    public void actionPerformed(ActionEvent e) {
        if (e.getSource() == chooseFileButton) {
            JFileChooser fileChooser = new JFileChooser();
            fileChooser.setFileSelectionMode(JFileChooser.DIRECTORIES_ONLY);

            int returnValue = fileChooser.showDialog(null, "Choose directory");
            if (returnValue == JFileChooser.APPROVE_OPTION) {
                File selectedDirectory = fileChooser.getSelectedFile();
                path_input.setText(selectedDirectory.getAbsolutePath());
            }
        }

        if (e.getSource() == start) {
            log.setText("");
            start.setEnabled(false);
            stop.setEnabled(true);
            TaskToBeSolved ttbs = new TaskToBeSolved();
            AnswersToBeChecked atbc = new AnswersToBeChecked();
            readThread = new ReadThread(path_input.getText(), ttbs);
            readThread.start();
            workingThread = new WorkingThread(ttbs, atbc, readThread);
            workingThread.start();
            checkThread = new CheckThread(log, start, stop, atbc, workingThread);
            checkThread.start();
        }

        if (e.getSource() == stop) {
            workingThread.stopThread();
            stop.setEnabled(false);
        }
    }
}
