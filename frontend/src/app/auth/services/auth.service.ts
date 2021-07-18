import { HttpClient } from '@angular/common/http'
import { Observable } from 'rxjs'
import { Injectable } from '@angular/core'
import { AuthResult, UserRegister, UserAuth } from '@/auth/models'
import { RegisterResult } from '@/auth/models/registerResult'


@Injectable( {
    providedIn: 'root'
} )
export class AuthService
{
    constructor( private http: HttpClient )
    {
    }

    auth( user: UserAuth ): AuthResult
    {
        return {
            error: null,
            isSuccessful: true
        }
    }

    createEmptyUser(): UserRegister
    {
        return {
            registerNumber: '',
            activationCode: '',
            email: '',
            password: '',
            name: '',
            lastName: '',
            birthDate: null,
            surname: ''
        }
    }

    register( user: UserRegister ): RegisterResult
    {
        return {
            error: null,
            isSuccessful: true
        }
    }
}