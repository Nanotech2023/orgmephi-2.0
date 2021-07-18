import { HttpClient } from '@angular/common/http'
import { Observable } from 'rxjs'
import { Injectable } from '@angular/core'
import { UserRegister } from '@/auth/models'
import { RegisterResult } from '@/auth/models/registerResult'


@Injectable( {
    providedIn: 'root'
} )
export class AuthService
{
    constructor( private http: HttpClient )
    {
    }

    //TODO return observable
    register( user: UserRegister ): RegisterResult
    {
        return {
            error: null,
            isSuccessful: true
        }
    }
}