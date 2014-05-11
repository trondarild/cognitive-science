/**
Information here


*/

import java.util.Deque;
import java.util.Random;
//
// parameters
//
int nback = 2;
float nbackprob = 0.5;
float changeinterval = 0.5;

String imgroot = "/../images/";
String year = String.valueOf(year());
String month = String.valueOf(month());
String day = String.valueOf(day());
String hour = String.valueOf(hour());
String minute = String.valueOf(minute());
String second = String.valueOf(second());
String timeformatstr = year + "-" + month + "-" + day + "_" + hour + ":" + minute + ":" + second;//"Y-%m-%d_%H:%M:%S";
//String logfilename = "data_" + timeformatstr + ".csv";
String logfiledir = "/../logs/";
String logheader = "time,image,nback,sessionid";

// difference in alpha value for each fade step
float fadestep = 0.15;
String startimgname = "/../startimg.png";
PImage startimage;
boolean fullscreen = false;

// globals
PrintWriter output;
String[] imgnames;
ArrayList<PImage> images;
Deque<PImage> dque;
boolean start = false;
int nbacknum = 0;
float fadecounter = 0;
int imgix = 0;
boolean imgchanged = false;
int sessionid = 0;
Random generator = new Random();

final int SPACE = 32;

// returns a string with current date to seconds resolution
String now(){
  String year = String.valueOf(year());
  String month = String.valueOf(month());
  String day = String.valueOf(day());
  String hour = String.valueOf(hour());
  String minute = String.valueOf(minute());
  String second = String.valueOf(second());
  
  //"Y-%m-%d_%H:%M:%S";
  String timeformatstr = year + "-" 
    + month + "-" 
    + day + "_" 
    + hour + ":" 
    + minute + ":" 
    + second;
    
  return timeformatstr;
  
}

// writes a sentence to logfile
void writeToLogFile(String sentence, PrintWriter logfile, boolean timestamp){
  String logitem = "";
  if(timestamp){
    logitem = now() + ","; 
  }
  logitem += sentence;
  
  // append to logfile
  logfile.println(logitem);
  logfile.flush();
}

// This function returns all the files in a directory as an array of Strings  
String[] listFileNames(String dir) {
  File file = new File(dir);  
  if (file != null && file.isDirectory()) {
    String names[] = file.list();
    return names;
  } else {
    // If it's not a directory
    return null;
  }
}

// loads and returns arraylist of images
ArrayList<PImage> loadImages(String path, String[] imagenames){

  ArrayList<PImage> retval = new ArrayList<PImage>();

  for (int i=0; i<imagenames.length; ++i){
    PImage img = loadImage(path + imagenames[i]);
    retval.add(img);
  }
  return retval;
}

// return default with probability prob, or a random number from
// 0 to max
int[] getProbIndex(int defaultIx, float prob, int max){
  boolean doDefault = getBinomial(1, prob) == 1;
  int[] retval = {defaultIx, 1};
  if(!doDefault) {
     // get a random number different from default
     int num = 0;
     while((num = generator.nextInt(max)) == defaultIx){}
     retval[0] = num; 
     retval[1] = 0;     
   } 
   return retval;
}

// gets a draw from binomial distribution
int getBinomial(int n, double p) {
  int x = 0;
  for(int i = 0; i < n; i++) {
    if(Math.random() < p)
      x++;
  }
  return x;
}

// fades picture
float fade(){
  float fadeval = 255.0*map(sin(fadecounter), -1, 1, 0, 1);
  //println(fadeval);
  tint(255, fadeval);
  fadecounter += fadestep;
  return map(fadeval, 0, 255, 0, 1);  
}

void setup(){
  imgnames = listFileNames(sketchPath + imgroot);
  images = loadImages(sketchPath + imgroot, imgnames);
  String logfilename = "data_" + now() + ".csv";
  output = createWriter(sketchPath + logfiledir + logfilename);
  //writeToLogFile(logheader, output, false);
  //writeToLogFile("one,two,three,four", output, false);
  
  background(0);
  size(1024, 768);
}

void draw(){
  background(0);
  fade();
  image(images.get(0), width/2, height/2);
  
}

void stop(){
  output.close();
}

void keyPressed(){
  if(keyCode == SPACE || keyCode == ENTER || keyCode == RETURN){
    println("hello");
  }  
}
