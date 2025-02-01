# **AetherMind**   
*A test project where I create an OpenAI-powered robotics system using Arduino or a computer-based platform.*  

## WARNING!! THIS IS THE DEV BRANCH OF **AetherMind**. USE AT YOUR OWN RISK, YOU HAVE BEEN WARNED.
### This branch is for experimental features. Nothing here is guaranteed to work.
### If you have suggestions, feel free to open an issue!

## **What is AetherMind?**  
AetherMind (Officially known as AetherMind AI) is an experimental AI robotics project where I integrate OpenAI’s API into a **computer-based AI system** and eventually **an Arduino-powered robot.**  

The first prototype, **Klaus**, is designed to have:  
**Memory persistence** – Stores and recalls previous conversations.  
**Conversational AI** – Uses OpenAI’s API to generate responses.  
**Future expansion** – Potential for **vision**, **hearing**, and **therapeutical listening**. Hearing is in the works right now!  

## Known issues!
### Speech recognition still unstable, investigating delays in TTS.

---

## **How to Use Klaus (First Prototype)**  
### **Requirements:**  
1️. **An OpenAI API key**  
2️. **A `.env` file containing the API key**  

3. **requirments.txt**  

### **Setup Instructions:**  
1. **Clone this repository:**  
   ```bash
   git clone https://github.com/TheAlepou/AetherMind.git
   cd AetherMind
   ```  
2. **Install dependencies:**  
   ```bash
   pip install -r requirements.txt
   ```  
3. **Create a `.env` file:**  
   - Open a text editor and create a new file named `.env`  
   - Add the following line (replace with your actual API key):  
     ```
     OPENAI_API_KEY=your_api_key_here
     ELEVENLABS_API_KEY=your_api_key_here
     ```  
   - Save the file.
4. **Install the dependencies:**
   ```run 
   pip install -r requirements.txt for the dependencies to install
   ```
5. **Run Klaus:**  
   ```bash
   python main.py
6. **Additional Steps**
   ```  
   On macOS: brew install portaudio
   On Linux: sudo apt-get install python3-pyaudio
   On Windows: No additional steps needed

   ```  

---

## **Future Plans & Roadmap**  
**Basic AI conversation system** *(Completed!)*  
**Basic Arduino implementation system** *(Completed!)*   
**Experiment with webcam, microphone, and speakers** *(In Progress, voice completed.)*  
**Potential integration of therapeutical listening** *(Currently working on it.)*  
**Potential future integration with Arduino for mobility inside cool plushies** *(Long-Term Goal)*  

---

## **Want to Contribute?**  
Right now, this is a **personal project**, but I may consider making it open-source for collaboration in the future!  

---

## License
This project is licensed under the **AGPL-3.0 License**.  
Any modifications, including web services using this software, must share their source code.

---

### **Final Thoughts**  
This is just the **beginning** of something huge. If you're interested in AI-driven robotics, stay tuned—**Klaus is evolving.**
