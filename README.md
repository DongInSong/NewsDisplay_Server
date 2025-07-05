# 탁상 뉴스 디스플레이 - 서버

## 프로젝트 정보

- 개발 기간: 2023. 02 - 2023. 06
- 개발 인원: 3명
- 개인 역할: 백엔드 설계 및 개발

  주요 기여 및 담당 업무
   * 서버
     - FastAPI 서버 구축 (원격서버: Pi, Ubuntu Server)
     - SQLAlchemy CRUD API 개발
       1. `models.py`: 데이터베이스 모델 1:1 매칭 
       2. `schemas.py`: API 출력 모델
       3. `crud.py`: SQLAlchemy query문
       4. ERD 설계 및 구축
       5. 원격 서버 리버스 프록시 (NginX)

## 1. ERD

![DB구조](https://github.com/user-attachments/assets/510a6185-d2d7-4123-b89e-8360b077158b)

## 2. API

![1_API](https://github.com/user-attachments/assets/d99c9768-7adb-41c0-afdb-38d9b3ab5484)

## 3. Model

![2_Model](https://github.com/user-attachments/assets/07b08255-ffa3-494b-9abb-fa7c81c1a8b2)

## 4. CRUD

![3_Crud](https://github.com/user-attachments/assets/8852d716-00c5-4894-bb40-7b83afeedf82)

## 5. Schemas

![4_Schemas](https://github.com/user-attachments/assets/6cf84971-c86b-485e-a873-951869f87f9d)

## 6. 설치 및 실행 방법

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

