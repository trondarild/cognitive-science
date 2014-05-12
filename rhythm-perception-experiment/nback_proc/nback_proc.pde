/**
Information here


*/

import java.util.ArrayDeque;
import java.util.Random;
//
// parameters
//
int nback = 2;
float nbackprob = 0.5;
float changeinterval = 0.5; 

String imgroot = "/../images/abstract/";
String logfiledir = "/../logs/";
String logheader = "time,image,nback,sessionid";

float framerate = 15;
float changetime = 1600;
float fadetime = 300;
float holdtime = changetime - 2*fadetime;
float fadestep = framerate*fadetime;
int sessionchanges = 10;

String startimgname = "/../startimage.png";
PImage startimage;
boolean fullscreen = false;

// globals
PrintWriter output;
String[] imgnames;
ArrayList<PImage> images;
ArrayDeque<Integer> dque;
boolean start = false;
int nbacknum = 0;
float fadecounter = 0;
int imgix = 0;
boolean imgchanged = false;
int sessionid = 0;
Random generator = new Random();
float frametime = 0;
int changecount = 0; 
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
float fade(float starttime, float fadetime, float holdtime) {
  float sincestart = millis() - starttime;
  float fadeval = 255;
  if(sincestart < fadetime) {
    // should fade in
    fadeval = map(sincestart/fadetime, 0, 1, 0, 255); 
  } else if(sincestart >= fadetime + holdtime) {
    // should fade out  
    fadeval = map((sincestart-(fadetime+holdtime))/fadetime, 0, 1, 255, 0); 
  }
  //float fadeval = 255.0*map(sin(fadecounter), -1, 1, 0, 1);
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
  imgix = int(random(0, images.size()));
  dque = new ArrayDeque<Integer>();
  dque.add(imgix);
  writeToLogFile(logheader, output, false);
  writeToLogFile(imgnames[imgix] + "," 
    + String.valueOf(nbacknum) + ","
    + String.valueOf(sessionid+1)
    , output, true  );
  frameRate(framerate);
  startimage = loadImage(sketchPath + startimgname);
  background(0);
  size(1280, 800 );
  frametime = millis();
}

void draw(){
  requestFocusInWindow();
  background(0);
  float timesince = millis() - frametime;
  if(changecount >= sessionchanges)
    start = false;
    
  if(start){
    float fadeval = fade(frametime, fadetime, holdtime);
    if(timesince >= changetime && !imgchanged){
      if(dque.size() >= nback){
        int nbackix = dque.remove().intValue();
        int[] probix = getProbIndex(nbackix, nbackprob, images.size());
        imgix = probix[0];
        nbacknum += probix[1];
        imgchanged = true;  
      } else {
        imgix = int(random(0, images.size())); 
      }
      writeToLogFile(imgnames[imgix] + "," 
        + String.valueOf(nbacknum) + ","
        + String.valueOf(sessionid)
        , output, true);
      dque.add(imgix);
      changecount++;
      frametime = millis();
    } else if(imgchanged && fadeval >= 0.01)
      imgchanged = false;
      
    //println(imgix);
    PImage img = images.get(imgix);
    image(img, width/2 - img.width/2, height/2 - img.height/2);
    
    // add sleep here
  } else {
    tint(255, 255);
    image(startimage, width/2 - startimage.width/2, height/2 - startimage.height/2);
    textSize(32);
    fill(127);
    String sessionstr = "Next session id = " + String.valueOf(sessionid + 1);
    float strwidth = textWidth(sessionstr);
    text(sessionstr, width/2 - strwidth/2.0, height/2 + startimage.height);
  }
}

void stop(){
  output.close();
}

void keyPressed(){
  if(keyCode == SPACE || keyCode == ENTER || keyCode == RETURN){
    if(!start){
      sessionid++;
      fadecounter = 0;
      nbacknum = 0;
      dque.clear();
      frametime = millis();
      changecount = 0;
      println("starting session" + String.valueOf(sessionid)); 
    }
    start = !start;
  }  
}

boolean sketchFullScreen(){
  return fullscreen;
}
