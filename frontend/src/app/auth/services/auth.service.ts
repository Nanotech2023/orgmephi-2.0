import { HttpClient } from '@angular/common/http'
import { Observable, of } from 'rxjs'
import { Injectable } from '@angular/core'
import { AuthResult, UserRegister, UserAuth } from '@/auth/models'
import { RegisterResult } from '@/auth/models/registerResult'
import { AuthSelectors, AuthState } from '@/auth/store'
import { select, Store } from '@ngrx/store'
import { map } from 'rxjs/operators'


@Injectable( {
    providedIn: 'root'
} )
export class AuthService
{
    constructor( private readonly store: Store<AuthState.State> )
    {
    }

    private readonly successResult: AuthResult | RegisterResult = { isSuccessful: true, error: '' }
    private readonly failedResult: AuthResult | RegisterResult = {
        isSuccessful: false,
        error: 'Неправильный email или пароль'
    }

    auth( user: UserAuth ): Observable<AuthResult>
    {
        return this.store.pipe(
            select( AuthSelectors.selectRegistration ),
            map(
                registration => this.getAuthResult( registration, user )
            )
        )
    }

    register( user: UserRegister ): Observable<RegisterResult>
    {
        return of( this.successResult )
    }

    private getAuthResult( registration: UserRegister | null, user: UserAuth )
    {
        if ( registration === null )
            return this.failedResult
        return registration !== null && user.email === registration.email && user.password == registration.password
            ? this.successResult
            : this.failedResult
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
}