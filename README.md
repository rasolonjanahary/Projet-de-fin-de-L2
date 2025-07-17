# Synthèse des datasets pour la 'prediction de taux de reussite au concours d'entré école/université'

---

## 1. admission_rate_ver_1.csv  
- **Source** : [https://dr-raz.org/statistical-literacy-csv-data](https://dr-raz.org/statistical-literacy-csv-data)  
- **Colonnes clés** : Serial No., GRE Score, TOEFL Score, University Rating, SOP, LOR, CGPA, Research, Chance of Admit  
- **Taille** : 400 lignes  
- **Note** : 75/100  
- **Respect du sujet** : Oui  
- **Commentaires** :  
  - La cible `Chance of Admit` est une estimation continue de la probabilité d’admission, adaptée à la prédiction.  
  - Données académiques complètes, mais absence d’informations socio-économiques ou motivationnelles détaillées.  
  - Taille moyenne, suffisante pour un modèle basique.  

---

## 2. gc_data.csv  
- **Source** : [https://sourceforge.net/projects/triangleinequal/files/Grad%20Cafe%20Data/gc_data.csv/download](https://sourceforge.net/projects/triangleinequal/files/Grad%20Cafe%20Data/gc_data.csv/download)  
- **Colonnes clés** : School, Program, Result, Result_Date, GPA, Verbal_GRE, Quant_GRE, Writing_GRE, Subject_GRE, Status, Submit_Date, Degree_Type  
- **Taille** : ~2000 lignes  
- **Note** : 80/100  
- **Respect du sujet** : Oui  
- **Commentaires** :  
  - Contient des résultats d’admission réels (`Result`), idéal pour prédiction binaire (admis/refusé).  
  - Beaucoup de données académiques sur les tests GRE, GPA, etc.  
  - Peu d’informations socio-économiques ou motivationnelles.  
  - Colonnes redondantes de dates à nettoyer.  

---

## 3. Predict students dropout and academic success  
- **Source** : [https://archive.ics.uci.edu/dataset/697/predict+students+dropout+and+academic+success](https://archive.ics.uci.edu/dataset/697/predict+students+dropout+and+academic+success)  
- **Colonnes clés** : Marital status, Application mode, Course, Previous qualification, Admission grade, Curricular units, Scholarship holder, Age at enrollment, Unemployment rate, Inflation, GDP, Target  
- **Taille** : 4000+ lignes  
- **Note** : 70/100  
- **Respect du sujet** : Partiellement oui  
- **Commentaires** :  
  - Très riche en variables socio-économiques et académiques.  
  - Pas de colonne explicite "admis/refusé" : cible à inférer (ex. `Admission grade`).  
  - Variables post-admission présentes (risque de fuite d’information).  
  - Nécessite un nettoyage important.  

---

## 4. Australian dataset  
- **Source** : [https://www.kaggle.com/datasets/nasirayub2/australian-student-performancedata-aspd24](https://www.kaggle.com/datasets/nasirayub2/australian-student-performancedata-aspd24) 
- **Colonnes clés** : 51 colonnes dont GPA, High School GPA, Entrance Exam Score, Attendance, Family Income, Parental Education, Health, Mental Health, Exam Scores, Performance  
- **Taille** : 10000  
- **Note** : 85/100  
- **Respect du sujet** : Oui  
- **Commentaires** :    
  - La colonne `Performance`est une observation de GPA , .... c'est à dire elle contient ('good',"poor","need improvement").  
  - Riche en variables explicatives, idéal pour un modèle avancé.  
  - Peu d’informations sur la source et taille exacte.  

---


