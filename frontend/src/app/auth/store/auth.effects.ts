import { Injectable } from '@angular/core'
import { Actions, createEffect, ofType } from '@ngrx/effects'
import { AuthService } from '@/auth/services/auth.service'
import {
    loginAttempt,
    loginError,
    loginSuccess,
    registerAttempt,
    registerError,
    registerSuccess
} from '@/auth/store/auth.actions'
import { catchError, concatMap, mergeMap } from 'rxjs/operators'
import { AuthResult, RegisterResult } from '@/auth/models'
import { iif, of } from 'rxjs'


// noinspection JSUnusedGlobalSymbols
@Injectable()
export class AuthEffects
{
    constructor( private actions$: Actions, private authService: AuthService )
    {
    }

    loginAttempt$ = createEffect( () =>
        this.actions$.pipe
        (
            ofType( loginAttempt ),
            concatMap( ( action ) =>
                this.authService.auth( action.user ).pipe(
                    mergeMap( ( authResult: AuthResult ) =>
                        iif( () => authResult.isSuccessful,
                            of( loginSuccess( {
                                user: { email: action.user.email, password: action.user.password }
                            } ) ),
                            of( loginError( {
                                result: { error: authResult.error, isSuccessful: false }
                            } ) )
                        ) ),
                    catchError(
                        error =>
                            of( loginError( { result: { error: error, isSuccessful: false } } ) )
                    )
                )
            )
        ) )

    registerAttempt$ = createEffect( () =>
        this.actions$.pipe
        (
            ofType( registerAttempt ),
            concatMap( ( action ) =>
                this.authService.register( action.registration ).pipe(
                    mergeMap( ( registerResult: RegisterResult ) =>
                        iif( () => registerResult.isSuccessful,
                            of( registerSuccess( {
                                registration: action.registration
                            } ) ),
                            of( registerError({
                                result: registerResult
                            }) )
                        )
                    )
                )
            )
        ) )
}