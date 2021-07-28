import { Injectable } from '@angular/core'
import { Actions, createEffect, ofType } from '@ngrx/effects'
import { AuthServiceMock } from '@/auth/api/auth.mock.service'
import { loginAttempt, loginError, loginSuccess, registerAttempt, registerSuccess } from '@/auth/store/auth.actions'
import { catchError, concatMap, mergeMap } from 'rxjs/operators'
import { of } from 'rxjs'
import { ResponseLogin, ResponseRegistration, TypeUserInfo } from '@/auth/models'
import { Router } from '@angular/router'


// noinspection JSUnusedGlobalSymbols
@Injectable()
export class AuthEffects
{
    constructor( private actions$: Actions, private authService: AuthServiceMock, private router: Router )
    {
    }

    loginAttempt$ = createEffect( () =>
        this.actions$.pipe
        (
            ofType( loginAttempt ),
            concatMap( ( { requestLogin } ) =>
                this.authService.loginPost( requestLogin ).pipe(
                    mergeMap( ( authResult: ResponseLogin ) =>
                        {
                            this.router.navigate( [ '/users' ] )
                            return of( loginSuccess( {
                                responseLogin: {
                                    // TODO CSRF Tokens???
                                    // csrfAccessToken: authResult.csrfAccessToken,
                                    // csrfRefreshToken: authResult.csrfRefreshToken
                                }
                            } ) )
                        }
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
            concatMap( ( { requestRegistration } ) =>
                this.authService.registerPost( requestRegistration ).pipe(
                    mergeMap( ( responseRegistration: ResponseRegistration ) =>
                        of( registerSuccess( { responseRegistration: responseRegistration } ) ) ),
                    catchError(
                        error =>
                            of( loginError( { error: error } ) )
                    )
                )
            )
        )
    )
}