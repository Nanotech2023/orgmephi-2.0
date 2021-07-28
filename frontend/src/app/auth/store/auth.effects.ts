import { Injectable } from '@angular/core'
import { Actions, createEffect, ofType } from '@ngrx/effects'
import { AuthServiceMock } from '@/auth/api/auth.mock.service'
import {
    loginAttempt,
    loginError,
    loginSuccess,
    pushPersonalInfo,
    registerAttempt,
    registerSuccess
} from '@/auth/store/auth.actions'
import { catchError, concatMap, mergeMap } from 'rxjs/operators'
import { of } from 'rxjs'
import { AuthResponse, CommonUserInfo } from '@/auth/models'


// noinspection JSUnusedGlobalSymbols
@Injectable()
export class AuthEffects
{
    constructor( private actions$: Actions, private authService: AuthServiceMock )
    {
    }

    loginAttempt$ = createEffect( () =>
        this.actions$.pipe
        (
            ofType( loginAttempt ),
            concatMap( ( { authentication } ) =>
                this.authService.loginPost( authentication ).pipe(
                    mergeMap( ( authResult: AuthResponse ) =>
                        of( loginSuccess( {
                            authResponse: {
                                csrfAccessToken: authResult.csrfAccessToken,
                                csrfRefreshToken: authResult.csrfRefreshToken
                            }
                        } ) )
                    ),
                    catchError(
                        error =>
                            of( loginError( { error: error } ) )
                    )
                )
            )
        )
    )

    registerAttempt$ = createEffect( () =>
        this.actions$.pipe
        (
            ofType( registerAttempt ),
            concatMap( ( action ) =>
                this.authService.registerPost( action.registration ).pipe(
                    mergeMap( ( registerResult: CommonUserInfo ) =>
                        of( registerSuccess( { commonUserInfo: registerResult } ) ) ),
                    catchError(
                        error =>
                            of( loginError( { error: error } ) )
                    )
                )
            )
        )
    )
}