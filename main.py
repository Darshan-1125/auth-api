from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from auth import supabase

app = FastAPI()


class AuthRequest(BaseModel):
    email: str
    password: str


@app.get("/")
def root():
    return {
        "message": "Server running and connected to Supabase"
    }


@app.post("/auth/signup", status_code=201)
def signup(request: AuthRequest):
    if not request.email or not request.password:
        raise HTTPException(
            status_code=400,
            detail="Email and password are required"
        )

    try:
        response = supabase.auth.sign_up({
            "email": request.email,
            "password": request.password
        })

        return {
            "message": "User created successfully",
            "user": response.user
        }

    except Exception as e:
        print("SUPABASE ERROR:", e)
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    

@app.post("/auth/login")
def login(request: AuthRequest):
    if not request.email or not request.password:
        raise HTTPException(
            status_code=400,
            detail="Email and password are required"
        )

    try:
        response = supabase.auth.sign_in_with_password({
            "email": request.email,
            "password": request.password
        })

        if not response.session:
            raise HTTPException(
                status_code=401,
                detail="Invalid login credentials"
            )

        return {
            "message": "Login successful",
            "access_token": response.session.access_token,
            "refresh_token": response.session.refresh_token
        }

    except HTTPException:
        raise

    except Exception:
        raise HTTPException(
            status_code=401,
            detail="Invalid login credentials"
        )