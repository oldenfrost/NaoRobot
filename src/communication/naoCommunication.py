# -*- encoding: UTF-8 -*- 

import base64
import openai
import speech_recognition as sr    

import time
import threading  

from naoqi import ALProxy
from movements.NaoMovements import NaoMovements
from utils.helpers import Helpers

class NaoCommunication:
    def __init__(self, ip, port, openAiKey, context):

        self.ip = ip
        self.port = port
        self.is_posing = False
        self.tts = ALProxy("ALTextToSpeech", ip, port)
        self.leds = ALProxy("ALLeds", ip, port)
        self.asp = ALProxy("ALAnimatedSpeech", ip, port)
        self.autonomusLife = ALProxy("ALAutonomousLife", ip, port)
        self.naoMovements  = NaoMovements(ip, port)
        self.memory = ALProxy("ALMemory", ip, port)
        self.context = context
        openai.api_key = base64.b64decode(openAiKey)
        self.memory.subscribeToEvent("FrontTactilTouched", "NaoCommunication", "OnFrontTouch")
        self.memory.subscribeToEvent("MiddleTactilTouched", "NaoCommunication", "OnMiddleTouch")
        self.memory.subscribeToEvent("BackTactilTouched", "NaoCommunication", "OnBackTouch")
        self.posingThread= None

#metodo inicial para que nao empiece su funcion 
    def Start(self, prompt):
            self.autonomusLife.setState("disabled")
            try:
                self.leds.on("AllLeds")
            except:
                print('Error de leds')
            self.naoMovements.stopEvent.set()
            self.posingThread = threading.Thread(target=self.naoMovements.StartPosing)
            self.posingThread.start()

            try:
                self.TalkNao(prompt, False)
            except Exception as e:
                self.naoMovements.stopEvent.clear()
                self.posingThread.join()
                print('Error: '+str(e))
            starMessage="Toca mi cabeza para comenzar mi funcio"
            self.asp.say(format(starMessage.encode('utf-8')))
            while True:
                headValue = self.memory.getData("FrontTactilTouched")
                MiddleValue = self.memory.getData("MiddleTactilTouched")
                BackValue = self.memory.getData("BackTactilTouched")
                if headValue:
                    self.OnFrontTouch()
                    break
                elif MiddleValue:
                    self.OnMiddleTouch()
                    break
                elif BackValue:
                    self.OnBackTouch()
                    break

#consulta api
    def GetOpenAIResponse(self, context, prompt):
        try:
            combinedPrompt=context + "\n" + prompt
            response = openai.Completion.create(
                engine="gpt-3.5-turbo-instruct",
                prompt=combinedPrompt,
            max_tokens=10
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
                    self.leds.setIntensity("AllLedsBlue", 0.5)
                except:
                    print('ErrorLeds')
                try:
                    print("Escuchando...")
                    print("por favor hable")
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

        if self.naoMovements.stopEvent.is_set() :
            self.naoMovements.stopEvent.clear()
            self.posingThread.join()

        option=self.AssignOption(prompt)
        if option:
            if option=="despedida":
                self.TalkNao(prompt, True)
                self.Finish()
                return
            elif option =="truco":
                self.naoMovements.Balance() 
            else:
                self.TalkNao(prompt, False)
                self.CreateAction(option,prompt)
        else:
            self.TalkNao(prompt, True)
        self.Listing()
 
#ejecuta la creacion de la accion respectiva segun el ejercicio  
    def CreateAction(self, exercise, prompt):
        self.autonomusLife.setState("disabled")   
        context="Proporcióname únicamente el número presente en el siguiente texto."
        response=self.GetOpenAIResponse(context.decode('utf-8').strip(), "'"+prompt+"'")
        response = response.strip()
        if response.isdigit():
            repetitions = int(response)
            self.StartExercise(exercise,repetitions)
        else:
            talk=u"No te escuché bien, bro, pero haré 3 reps."
            self.asp.say("^start(animations/Stand/Gestures/Me_1) {} ^wait(animations/Stand/Gestures/Me_1)".format(talk.encode('utf-8')))
            time.sleep(1)
            self.StartExercise(exercise,3)
            

#inicializa el llamado de los metodos para realizar los ejercicios
    def StartExercise(self, exercise, repetitions):
        repetition=0
        exerciseDetails=self.GetExerciseDetails(exercise)
        method = getattr(self.naoMovements,exerciseDetails[0],None)
        method()
        for _ in range(repetitions):
            method = getattr(self.naoMovements,exerciseDetails[1],None)
            method()
            method = getattr(self.naoMovements,exerciseDetails[2],None)
            method()
            repetition += 1 
            self.tss.say(format(repetition))
        self.naoMovements.SetPosition(exerciseDetails[3])
        if exerciseDetails[3]=="LyingBelly":
            self.naoMovements.SetPosition("Crouch")
        self.naoMovements.SetPosition("Stand")
        

#obtine los metodos para cada ejercicios      
    def GetExerciseDetails(self, exercise):
        switch = {
            'sentadillas': ['StartPositionSquad', 'SquatsDown', 'SquatsUp', 'StandZero'],
            'abdominales': ['StartPositionCrunch', 'SitDonw', 'SitUp', 'Sit'],
            'lagartijas': ['StartPositionPushUp', 'PushDonw', 'PushUp','LyingBelly']
        }
        return switch.get(exercise, ['default_action'])
    
    def TalkNao(self,prompt, active):
        talk=self.GetOpenAIResponse(self.context, prompt)
        if active:
            self.autonomusLife.setState("interactive")
            self.asp.say("^start(animations/Stand/Gestures/Me_1) {} ^wait(animations/Stand/Gestures/Me_1)".format(talk.encode('utf-8')))
        else:
            self.tts.say(format(talk.encode('utf-8')))



    def AssignOption(self,prompt):
        promptLower=prompt.lower()
        optionFound=None
        keywordsDict = Helpers.GetKeywords()

        for option, words in keywordsDict.items():
            if any(word.decode('utf-8').lower() in promptLower for word in words):
               optionFound = option 
               break
        return optionFound


    def Finish(self):
        self.autonomusLife.setState("disabled")
        try:
            self.leds.off('AllLeds')
        except Exception:
            print('Error al apagar leds')  
        self.naoMovements.StiffnessOff()

    
    def OnFrontTouch(self):
            self.Listing()

    def OnMiddleTouch(self):
            self.Finish(self)
            self.Start("presentate")
     

    def OnBackTouch(self):
            if self.naoMovements.stopEvent.is_set() :
                self.naoMovements.stopEvent.clear()
                self.posingThread.join()
            self.Finish(self)
            self.memory.unsubscribeToEvent("FrontTactilTouched", "NaoCommunication")
            self.memory.unsubscribeToEvent("OnMiddleTouch", "NaoCommunication")
            self.memory.unsubscribeToEvent("OnBackTouch", "NaoCommunication")


            




    



    






       




 

    


        



        

        

        

        
    
       
        
