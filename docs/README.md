# **AetherMind**  
*A cutting-edge AI-powered robotics system integrating OpenAI’s API with Arduino and computer-based platforms.*  

## ⚠️ WARNING: **EXPERIMENTAL DEV BRANCH** ⚠️  
This is the development branch of **AetherMind**. Features here are experimental, unstable, and may not work as expected. **Use at your own risk!**  
If you encounter issues or have suggestions, feel free to open an issue!

---

## **What is AetherMind?**  
AetherMind (officially **AetherMind AI**) is an experimental **AI robotics** project that integrates OpenAI’s API into a **computer-based AI system**, with plans for **Arduino-powered robotics**.  

The **debate prototype**, **Astra**, is designed for:
✅ **Memory Persistence** – Stores and recalls previous conversations.  
✅ **Conversational AI** – Uses OpenAI’s API to generate responses.  
✅ **Future Expansion** – Plans to integrate **vision**, **hearing**, and **therapeutic listening**. *(Hearing is currently in development!)*  

### **Known Issues 🚨**
- 🛠️ **Speech recognition is unstable** (delays in TTS still under investigation).  

---

## **How to Use Astra (First Prototype)**  
### **Requirements:**  
- **Python 3.9.X**  
- **An OpenAI API key**  
- **An ElevenLabs API key**  
- **A `.env` file containing the API keys**  
- **Required dependencies (listed in `requirements.txt`)**  

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
   - Add the following lines (replace with your actual API keys):  
     ```
     OPENAI_API_KEY=your_api_key_here
     ELEVENLABS_API_KEY=your_api_key_here
     ```  
   - Save the file.  
4. **Run Astra:**  
   ```bash
   python main.py
   ```  
5. **Additional Dependencies (OS-Specific):**  
   ```bash
   # macOS
   brew install portaudio
   
   # Linux
   sudo apt-get install python3-pyaudio
   
   # Windows
   # No additional dependencies required
   ```  

---

## **Future Plans & Roadmap 🛠️**  
✅ **Basic AI conversation system** *(Completed!)*  
✅ **Basic Arduino integration** *(Completed!)*  
🔄 **Experimenting with webcam, microphone, and speakers** *(In Progress: Voice & hearing completed!)*  
---

## **Want to Contribute?**  
Currently, **AetherMind** is a personal project, but contributions may be welcomed in the future! Stay tuned.  

---

## **License 📜**  
This project is licensed under the **AGPL-3.0 License**.  
Any modifications, including web services using this software, must share their source code.  

---

🚀 **AetherMind is just getting started! Stay curious, experiment, and push the boundaries of AI robotics!**
