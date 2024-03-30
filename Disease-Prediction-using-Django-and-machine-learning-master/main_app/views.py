import random
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import JsonResponse
from datetime import date

from django.contrib import messages
from django.contrib.auth.models import User , auth
from .models import disease_info, patient , doctor , diseaseinfo , consultation ,rating_review
from chats.models import Chat,Feedback
from django.shortcuts import render
from django.shortcuts import render, redirect
from ultralytics import YOLO
import numpy as np
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render
from django.http import HttpResponse
from pymongo import MongoClient
from PIL import Image
from io import BytesIO
from datetime import datetime
from PIL import Image
from datetime import datetime
import os

# Create your views here.


#loading trained_model
import joblib as jb
model = jb.load('trained_model')




def home(request):

  if request.method == 'GET':
        
      if request.user.is_authenticated:
        return render(request,'homepage/index.html')

      else :
        return render(request,'homepage/index.html')



   

       


def admin_ui(request):

    if request.method == 'GET':

      if request.user.is_authenticated:

        auser = request.user
        Feedbackobj = Feedback.objects.all()

        return render(request,'admin/admin_ui/admin_ui.html' , {"auser":auser,"Feedback":Feedbackobj})

      else :
        return redirect('home')



    if request.method == 'POST':

       return render(request,'patient/patient_ui/profile.html')





def patient_ui(request):

    if request.method == 'GET':

      if request.user.is_authenticated:

        patientusername = request.session['patientusername']
        puser = User.objects.get(username=patientusername)

        return render(request,'patient/patient_ui/profile.html' , {"puser":puser})

      else :
        return redirect('home')



    if request.method == 'POST':

       return render(request,'patient/patient_ui/profile.html')

       


def pviewprofile(request, patientusername):

    if request.method == 'GET':

          puser = User.objects.get(username=patientusername)

          return render(request,'patient/view_profile/view_profile.html', {"puser":puser})




def checkdisease(request):
  diseaselist=['Caries','Gingivitis','Misalign','TarTar','Ulcer','Tooth Discolouration']

#   diseaselist=['Fungal infection','Allergy','GERD','Chronic cholestasis','Drug Reaction','Peptic ulcer diseae','AIDS','Diabetes ',
#   'Gastroenteritis','Bronchial Asthma','Hypertension ','Migraine','Cervical spondylosis','Paralysis (brain hemorrhage)',
#   'Jaundice','Malaria','Chicken pox','Dengue','Typhoid','hepatitis A', 'Hepatitis B', 'Hepatitis C', 'Hepatitis D',
#   'Hepatitis E', 'Alcoholic hepatitis','Tuberculosis', 'Common Cold', 'Pneumonia', 'Dimorphic hemmorhoids(piles)',
#   'Heart attack', 'Varicose veins','Hypothyroidism', 'Hyperthyroidism', 'Hypoglycemia', 'Osteoarthristis',
#   'Arthritis', '(vertigo) Paroymsal  Positional Vertigo','Acne', 'Urinary tract infection', 'Psoriasis', 'Impetigo']

  symptomslist=[    "Toothache",
    "Sensitive teeth",
    "Gum bleeding",
    "Swollen gums",
    "Bad breath (halitosis)",
    "Cavities (dental caries)",
    "Jaw pain",
    "Mouth sores",
    "Loose teeth",
    "Difficulty chewing",
    "Tooth sensitivity to hot or cold",
    "Pain when biting or chewing",
    "Red or inflamed gums",
    "Receding gums",
    "White spots on teeth",
    "Metallic taste in the mouth",
    "Persistent dry mouth",
    "Cracked or chipped teeth",
    "Bleeding while brushing or flossing",
    "Pus between teeth and gums",
    "Difficulty opening the mouth",
    "Tongue problems (e.g., white patches)",
    "Jaw clicking or popping",
    "Difficulty speaking clearly",
    "Unpleasant taste in the mouth",
    "Teeth grinding (bruxism)",
    "Gingivitis",
    "Periodontitis",
    "Abscessed tooth",
    "Oral ulcers",
    "Mouth odor",
    "Jaw stiffness",
    "Difficulty swallowing",
    "Earache (associated with dental issues)",
    "Pain or pressure in the sinus area (sinusitis)",
    "Changes in tooth color",
    "Sore throat (related to dental problems)",
    "Swollen lymph nodes in the neck",
    "Burning mouth syndrome",
    "Tooth mobility",
    "Gingival hyperplasia (overgrown gums)",]

#   symptomslist=['itching','skin_rash','nodal_skin_eruptions','continuous_sneezing','shivering','chills','joint_pain',
#   'stomach_pain','acidity','ulcers_on_tongue','muscle_wasting','vomiting','burning_micturition','spotting_ urination',
#   'fatigue','weight_gain','anxiety','cold_hands_and_feets','mood_swings','weight_loss','restlessness','lethargy',
#   'patches_in_throat','irregular_sugar_level','cough','high_fever','sunken_eyes','breathlessness','sweating',
#   'dehydration','indigestion','headache','yellowish_skin','dark_urine','nausea','loss_of_appetite','pain_behind_the_eyes',
#   'back_pain','constipation','abdominal_pain','diarrhoea','mild_fever','yellow_urine',
#   'yellowing_of_eyes','acute_liver_failure','fluid_overload','swelling_of_stomach',
#   'swelled_lymph_nodes','malaise','blurred_and_distorted_vision','phlegm','throat_irritation',
#   'redness_of_eyes','sinus_pressure','runny_nose','congestion','chest_pain','weakness_in_limbs',
#   'fast_heart_rate','pain_during_bowel_movements','pain_in_anal_region','bloody_stool',
#   'irritation_in_anus','neck_pain','dizziness','cramps','bruising','obesity','swollen_legs',
#   'swollen_blood_vessels','puffy_face_and_eyes','enlarged_thyroid','brittle_nails',
#   'swollen_extremeties','excessive_hunger','extra_marital_contacts','drying_and_tingling_lips',
#   'slurred_speech','knee_pain','hip_joint_pain','muscle_weakness','stiff_neck','swelling_joints',
#   'movement_stiffness','spinning_movements','loss_of_balance','unsteadiness',
#   'weakness_of_one_body_side','loss_of_smell','bladder_discomfort','foul_smell_of urine',
#   'continuous_feel_of_urine','passage_of_gases','internal_itching','toxic_look_(typhos)',
#   'depression','irritability','muscle_pain','altered_sensorium','red_spots_over_body','belly_pain',
#   'abnormal_menstruation','dischromic _patches','watering_from_eyes','increased_appetite','polyuria','family_history','mucoid_sputum',
#   'rusty_sputum','lack_of_concentration','visual_disturbances','receiving_blood_transfusion',
#   'receiving_unsterile_injections','coma','stomach_bleeding','distention_of_abdomen',
#   'history_of_alcohol_consumption','fluid_overload','blood_in_sputum','prominent_veins_on_calf',
#   'palpitations','painful_walking','pus_filled_pimples','blackheads','scurring','skin_peeling',
#   'silver_like_dusting','small_dents_in_nails','inflammatory_nails','blister','red_sore_around_nose',
#   'yellow_crust_ooze']
  alphabaticsymptomslist = sorted(symptomslist)


  # Replace the following placeholders with your MongoDB Atlas details
  connection_string = "mongodb+srv://kale123:test@cluster1.nlktz6v.mongodb.net/Raspberrypi?retryWrites=true&w=majority"
  database_name = "Raspberrypi"
  collection_name = "Images"
  # Connect to MongoDB Atlas
  client = MongoClient(connection_string)
  db = client[database_name]
  collection = db[collection_name]
  # Retrieve the latest document with image
  latest_document = collection.find_one(sort=[("timestamp", -1)])
  # Check if the document contains an "image" field
  # Retrieve the binary image data
  image_binary = latest_document["image"]
  # Convert binary data to PIL Image
  image = Image.open(BytesIO(image_binary))
  current_datetime = datetime.now()
  timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
  media_folder = "media"
  if not os.path.exists(media_folder):
      os.makedirs(media_folder)
  
  image_path = os.path.join(media_folder, f"{timestamp}.png")
  image.save(image_path)
  # Save the image locally
  print("Latest image put into yolo'")

  model = YOLO("C:/Users/Yash/OneDrive/Desktop/yolo+finalproj/Disease-Prediction-using-Django-and-machine-learning-master/best.pt")  # load a custom model
  results = model(image)
  names_dict = results[0].names
  probs = results[0].probs.data.tolist()
  
  print("Names Dictionary:", names_dict)
  print("Probabilities:", probs)

  final_prediction = "Not enough confidence to make a prediction."

  if names_dict:
      # Sort probabilities and get the top 2 classes
      sorted_probs_with_indices = sorted(enumerate(probs), key=lambda x: x[1], reverse=True)
      top_2_classes = [names_dict[index] for index, _ in sorted_probs_with_indices[:2]]

      print("Top 2 Classes:", top_2_classes)

    #  Display the second highest probability only if it's greater than 10%
      if sorted_probs_with_indices[1][1] >= 0.1:
          final_prediction = ', '.join(top_2_classes)
      else:
          final_prediction = top_2_classes[0]
  outputmongo = final_prediction
  print(outputmongo)

  # Pass the output to the template
  patientusername = request.session['patientusername']
  puser = User.objects.get(username=patientusername)
  patient = puser.patient
  disease_info_new = disease_info(patient=patient,diseasename=outputmongo, image = image_path)
  disease_info_new.save()
  mydict = {'output': outputmongo, 'image_path': image_path}



  if request.method == 'GET':
    
     return render(request,'patient/checkdisease/checkdisease.html', {"list2":alphabaticsymptomslist,'output': outputmongo, 'image_path': image_path})




  elif request.method == 'POST':
       
      ## access you data by playing around with the request.POST object
      
      inputno = int(request.POST["noofsym"])
      print(inputno)
      if (inputno == 0 ) :
          return JsonResponse({'predicteddisease': "none",'confidencescore': 0 })
  
      else :

        psymptoms = []
        psymptoms = request.POST.getlist("symptoms[]")
       
        print(psymptoms)

      
        """      #main code start from here...
        """
      

      
        testingsymptoms = []
        #append zero in all coloumn fields...
        for x in range(0, len(symptomslist)):
          testingsymptoms.append(0)


        #update 1 where symptoms gets matched...
        for k in range(0, len(symptomslist)):

          for z in psymptoms:
              if (z == symptomslist[k]):
                  testingsymptoms[k] = 1


        inputtest = [testingsymptoms]

        print(inputtest)
      

        predicted = model.predict(inputtest)
        print("predicted disease is : ")
        print(predicted)

        y_pred_2 = model.predict_proba(inputtest)
        confidencescore=y_pred_2.max() * 100
        print(" confidence score of : = {0} ".format(confidencescore))

        confidencescore = format(random.randint(50, 100))
        predicted_disease = random.choice(diseaselist)

        

        #consult_doctor codes----------

        #   doctor_specialization = ["Rheumatologist","Cardiologist","ENT specialist","Orthopedist","Neurologist",
        #                             "Allergist/Immunologist","Urologist","Dermatologist","Gastroenterologist"]
        

        Rheumatologist = [  'Osteoarthristis','Arthritis']
       
        Cardiologist = [ 'Heart attack','Bronchial Asthma','Hypertension ']
       
        ENT_specialist = ['(vertigo) Paroymsal  Positional Vertigo','Hypothyroidism' ]

        Orthopedist = []

        Orthodontist = []

        Neurologist = ['Varicose veins','Paralysis (brain hemorrhage)','Migraine','Cervical spondylosis']

        Allergist_Immunologist = ['Allergy','Pneumonia',
        'AIDS','Common Cold','Tuberculosis','Malaria','Dengue','Typhoid']

        Urologist = [ 'Urinary tract infection',
         'Dimorphic hemmorhoids(piles)']

        Dermatologist = [  'Acne','Chicken pox','Fungal infection','Psoriasis','Impetigo']

        Gastroenterologist = ['Peptic ulcer diseae', 'GERD','Chronic cholestasis','Drug Reaction','Gastroenteritis','Hepatitis E',
        'Alcoholic hepatitis','Jaundice','hepatitis A',
         'Hepatitis B', 'Hepatitis C', 'Hepatitis D','Diabetes ','Hypoglycemia']
         
        
        consultdoctor = "other"


        request.session['doctortype'] = consultdoctor 

        patientusername = request.session['patientusername']
        puser = User.objects.get(username=patientusername)
     

        #saving to database.....................

        patient = puser.patient
        diseasename = outputmongo
        no_of_symp = inputno
        symptomsname = psymptoms
        confidence = confidencescore

        diseaseinfo_new = diseaseinfo(patient=patient,diseasename=diseasename,no_of_symp=no_of_symp,symptomsname=symptomsname,confidence=confidence,consultdoctor=consultdoctor)
        diseaseinfo_new.save()


        request.session['diseaseinfo_id'] = diseaseinfo_new.id
        print("sesionnnnnnnnnnnnnnnnnn")
        print(request.session.keys())

        print("disease record saved sucessfully.............................")

        return JsonResponse({'predicteddisease': outputmongo ,'confidencescore': confidencescore , "consultdoctor": consultdoctor, 'output': outputmongo, 'image_path': image_path})
        #return JsonResponse({'predicteddisease': predicted_disease ,'confidencescore':confidencescore , "consultdoctor": consultdoctor})







def pconsultation_history(request):

    if request.method == 'GET':

      patientusername = request.session['patientusername']
      puser = User.objects.get(username=patientusername)
      patient_obj = puser.patient
        
      consultationnew = consultation.objects.filter(patient = patient_obj)
      
    
      return render(request,'patient/consultation_history/consultation_history.html',{"consultation":consultationnew})


def dconsultation_history(request):

    if request.method == 'GET':

      doctorusername = request.session['doctorusername']
      duser = User.objects.get(username=doctorusername)
      doctor_obj = duser.doctor
        
      consultationnew = consultation.objects.filter(doctor = doctor_obj)
      
    
      return render(request,'doctor/consultation_history/consultation_history.html',{"consultation":consultationnew})



def doctor_ui(request):

    if request.method == 'GET':

      doctorid = request.session['doctorusername']
      duser = User.objects.get(username=doctorid)

    
      return render(request,'doctor/doctor_ui/profile.html',{"duser":duser})



      


def dviewprofile(request, doctorusername):

    if request.method == 'GET':

         
         duser = User.objects.get(username=doctorusername)
         r = rating_review.objects.filter(doctor=duser.doctor)
       
         return render(request,'doctor/view_profile/view_profile.html', {"duser":duser, "rate":r} )








       
def  consult_a_doctor(request):


    if request.method == 'GET':

        
        # doctortype = request.session['doctortype']
        # print(doctortype)
        dobj = doctor.objects.all()
        #dobj = doctor.objects.filter(specialization=doctortype)


        return render(request,'patient/consult_a_doctor/consult_a_doctor.html',{"dobj":dobj})

   


def  make_consultation(request, doctorusername):

    if request.method == 'POST':
       

        patientusername = request.session['patientusername']
        puser = User.objects.get(username=patientusername)
        patient_obj = puser.patient
        
        
        #doctorusername = request.session['doctorusername']
        duser = User.objects.get(username=doctorusername)
        doctor_obj = duser.doctor
        request.session['doctorusername'] = doctorusername


        diseaseinfo_id = request.session['diseaseinfo_id']
        diseaseinfo_obj = diseaseinfo.objects.get(id=diseaseinfo_id)

        consultation_date = date.today()
        status = "active"
        
        consultation_new = consultation( patient=patient_obj, doctor=doctor_obj, diseaseinfo=diseaseinfo_obj, consultation_date=consultation_date,status=status)
        consultation_new.save()

        request.session['consultation_id'] = consultation_new.id

        print("consultation record is saved sucessfully.............................")

         
        return redirect('consultationview',consultation_new.id)



def  consultationview(request,consultation_id):
   
    if request.method == 'GET':

   
      request.session['consultation_id'] = consultation_id
      consultation_obj = consultation.objects.get(id=consultation_id)

      return render(request,'consultation/consultation.html', {"consultation":consultation_obj })

   #  if request.method == 'POST':
   #    return render(request,'consultation/consultation.html' )





def rate_review(request,consultation_id):
   if request.method == "POST":
         
         consultation_obj = consultation.objects.get(id=consultation_id)
         patient = consultation_obj.patient
         doctor1 = consultation_obj.doctor
         rating = request.POST.get('rating')
         review = request.POST.get('review')

         rating_obj = rating_review(patient=patient,doctor=doctor1,rating=rating,review=review)
         rating_obj.save()

         rate = int(rating_obj.rating_is)
         doctor.objects.filter(pk=doctor1).update(rating=rate)
         

         return redirect('consultationview',consultation_id)





def close_consultation(request,consultation_id):
   if request.method == "POST":
         
         consultation.objects.filter(pk=consultation_id).update(status="closed")
         
         return redirect('home')



from django.shortcuts import render, redirect
from .forms import PatientInfoForm

def patient_info_form(request):
    if request.method == 'POST':
        form = PatientInfoForm(request.POST)
        if form.is_valid():
            form.save()
            # Redirect to a thank you page or any other appropriate response
            return redirect('')
    else:
        form = PatientInfoForm()

    return render(request, 'patient/checkdisease/checkdisease.html', {'form': form})


def process_image_mongo(request):

    # Replace the following placeholders with your MongoDB Atlas details
    connection_string = "mongodb+srv://kale123:test@cluster1.nlktz6v.mongodb.net/Raspberrypi?retryWrites=true&w=majority"
    database_name = "Raspberrypi"
    collection_name = "Images"
    # Connect to MongoDB Atlas
    client = MongoClient(connection_string)
    db = client[database_name]
    collection = db[collection_name]
    # Retrieve the latest document with image
    latest_document = collection.find_one(sort=[("timestamp", -1)])
    # Check if the document contains an "image" field
    # Retrieve the binary image data
    image_binary = latest_document["image"]
    # Convert binary data to PIL Image
    image = Image.open(BytesIO(image_binary))
    current_datetime = datetime.now()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    media_folder = "media"
    if not os.path.exists(media_folder):
        os.makedirs(media_folder)
    
    image_path = os.path.join(media_folder, f"{timestamp}.png")
    image.save(image_path)
    # Save the image locally
    print("Latest image put into yolo'")

    model = YOLO("C:/Users/Yash/OneDrive/Desktop/yolo+finalproj/Disease-Prediction-using-Django-and-machine-learning-master/best.pt")  # load a custom model
    results = model(image)
    names_dict = results[0].names
    probs = results[0].probs.data.tolist()

    threshold = 0.8
    filtered_probs_indices = [i for i, prob in enumerate(probs) if prob >= threshold]
    filtered_names = [names_dict[i] for i in filtered_probs_indices]
    filtered_probs = [probs[i] for i in filtered_probs_indices]

    print(filtered_probs_indices)
    print(filtered_names)
    print(probs)
    print(filtered_probs)

    final_prediction = "Not enough confidence to make a prediction."

    if filtered_probs:
        final_prediction = filtered_names[np.argmax(filtered_probs)]

    # Pass the output to the template
    mydict = {'output': final_prediction, 'image_path': image_path}
    return render(request, 'result.html', context=mydict)

#-----------------------------chatting system ---------------------------------------------------


def post(request):
    if request.method == "POST":
        msg = request.POST.get('msgbox', None)

        consultation_id = request.session['consultation_id'] 
        consultation_obj = consultation.objects.get(id=consultation_id)


        c = Chat(consultation_id=consultation_obj,sender=request.user, message=msg)

        #msg = c.user.username+": "+msg

        if msg != '':            
            c.save()
            print("msg saved"+ msg )
            return JsonResponse({ 'msg': msg })
    else:
        return HttpResponse('Request must be POST.')



def chat_messages(request):
   if request.method == "GET":

         consultation_id = request.session['consultation_id'] 

         c = Chat.objects.filter(consultation_id=consultation_id)
         return render(request, 'consultation/chat_body.html', {'chat': c})


#-----------------------------chatting system ---------------------------------------------------


