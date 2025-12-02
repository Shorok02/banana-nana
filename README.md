# banana-nana

## to run the code do the following , after cloning the project: ; 

### 1- create a .env file in the **root directory** and include in it the code below 

    **banana-nana\.env**:
    
    GROQ_API_KEY=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
    
    ALLOWED_EXTENSIONS = {".txt", ".pdf", ".docx"}
    
    MAX_SIZE_MB = 50 * 1024 * 1024

### 2- create a .env.local filein the **frontend** and add include in it the code below 

    **banana-nana\Frontend\.env.local**: 
    
    NEXT_PUBLIC_API_URL=http://127.0.0.1:8000
    
    GOOGLE_CLIENT_ID=1053522225541-mjtajva9itdoqk9rldeqdscs0171a7bp.apps.googleusercontent.com
    
    GOOGLE_CLIENT_SECRET=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
    
    NEXTAUTH_URL=http://localhost:3000  

    NEXTAUTH_SECRET=some-random-secret  

### 3- run **docker compose up --build**

## documentation is available through swagger : 
http://127.0.0.1:8000/docs

