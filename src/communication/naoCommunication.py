# -*- encoding: UTF-8 -*- 

import base64
import openai
import speech_recognition as sr    

import time
import threading  

from naoqi import ALProxy
from movements.NaoMovements import NaoMovements

class NaoCommunication:
    def __init__(self, ip, port, openAiKey, context):

        self.ip = ip
        self.port = port
        self.is_posing = False
        self.tts = ALProxy("ALTextToSpeech", ip, port)
        self.leds = ALProxy("ALLeds", ip, port)
        self.asp = ALProxy("ALAnimatedSpeech", ip, port)
        self.naoMovements  = NaoMovements(ip, port)
        self.context = context
        openai.api_key = base64.b64decode(openAiKey)

#metodo inicial para que nao empiece su funcion 
    def Start(self, prompt):
      
        self.tts.setLanguage("Spanish")
        self.tts.setVoice("maki_n16")
        try:
            self.leds.on("AllLeds")
        except:
            print('Error de leds')

        posingThread = threading.Thread(target=self.naoMovements.StartPosing)
        posingThread.start()
        talk=self.NaoTalk(self.context, prompt)    
        self.asp.say("^start(animations/Stand/Gestures/Me_1) {} ^wait(animations/Stand/Gestures/Me_1)".format(talk.encode('utf-8')))
        #print(talk)
        #listingThread = threading.Thread(target=self.naoMovements.StartPosing)
        #listingThread.start()
        self.Listing()

#consulta api
    def NaoTalk(self, context,prompt):
        try:
            combinedPrompt=context + "\n" + prompt
            response = openai.Completion.create(
                engine="gpt-3.5-turbo-instruct",
                prompt=combinedPrompt,
            max_tokens=300
            )
            return response.choices[0].text.strip()
        except Exception as e:
            return "los siento Hermano pero hubo un problema con consulta del api de openai" + str(e)
        
#ejecuta el listing
    def Listing(self):
        recognizer = sr.Recognizer("es-cr") 
        inputText = ""

        while True:
            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source, duration=1)
                try:
                # Control de los LEDs
                    self.leds.setIntensity("AllLeds", 0)
                    self.leds.setIntensity("AllLedsBlue", 0.9)
                except:
                    print('ErrorLeds')

                try:
                    print("Escuchando...")
                    audio = recognizer.listen(source, timeout=3)
                except OSError:
                    continue

            try:
                inputText = recognizer.recognize(audio)
            except LookupError:
                print("Voz no detectada\n")
            if inputText:
                break

        if isinstance(inputText, str):
            prompt = inputText.decode('utf-8').strip()
        else:
            prompt = inputText.strip()
        
        print(prompt)

        #response = self.NaoTalk(prompt)
        #print(response)

        if "squats" in prompt or "sentadilla" in prompt:
            exercise="squats"
            self.CreateAction(exercise,prompt)
        if "sit up" in prompt or "abdominales" in prompt:
            exercise="sitUp"
            self.CreateAction(exercise,prompt)
        if "PushUp" in prompt or "lagartijas" in prompt:
            exercise="pushUp"
            self.CreateAction(exercise,prompt)
       

#ejecuta la creacion de la accion respectiva segun el ejercicio  
    def CreateAction(self, exercise, prompt):

        context="Proporcióname únicamente el número presente en el siguiente texto."
        response=self.NaoTalk(context.decode('utf-8').strip(), "'"+prompt+"'")
        response = response.strip()
        if response.isdigit():
            repetitions = int(response)
            self.StartExercise(exercise,repetitions)
        else:
            talk=u"No te escuché bien, bro, pero haré 3 reps."
            self.asp.say("^start(animations/Stand/Gestures/Me_1) {} ^wait(animations/Stand/Gestures/Me_1)".format(talk.encode('utf-8')))
            self.StartExercise(exercise,3)
            

#inicializa el llamado de los metodos para realizar los ejercicios
    def StartExercise(self, exercise, repetitions):
        repetition=0
        exerciseDetails=self.GetExerciseDetails(exercise)
        self.naoMovements.StartPositionExercise(exerciseDetails[0])
        for _ in range(repetitions):
            method = getattr(self.naoMovements,exerciseDetails[1],None)
            method()
            method = getattr(self.naoMovements,exerciseDetails[2],None)
            method()
            repetition += 1 
            self.asp.say("^start(animations/Stand/Gestures/Me_1) {} ^wait(animations/Stand/Gestures/Me_1)".format(repetition))
    
        if exerciseDetails[0]!="Crouch":
            self.naoMovements.StartPositionExercise(exerciseDetails[0])
        else:
            self.naoMovements.EndPositionPushUp(exerciseDetails[0])

#obtine los metodos para cada ejercicios      
    def GetExerciseDetails(self, exercise):
        switch = {
            'squats': ['Stand', 'SquatsDown', 'SquatsUp'],
            'sitUp': ['Sit', 'SitDonw', 'SitUp'],
            'pushUp': ['Crouch', 'PushDonw', 'PushUp']
        }
        return switch.get(exercise, ['default_action'])
    

 

    


        



        

        

        

        
    
       
        
