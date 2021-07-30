import { Injectable } from '@angular/core'
import { Actions, createEffect, ofType } from '@ngrx/effects'
import { AuthServiceReal } from '@/auth/api/auth.service.real'
import { loginAttempt, loginError, loginSuccess, registerAttempt, registerSuccess } from '@/auth/store/auth.actions'
import { catchError, concatMap, mergeMap } from 'rxjs/operators'
import { of } from 'rxjs'
import { TypeCSRFPair, TypeUserInfo } from '@/auth/api/models'
import { Router } from '@angular/router'


// noinspection JSUnusedGlobalSymbols
@Injectable()
export class AuthEffects
{
    constructor( private actions$: Actions, private authService: AuthServiceReal, private router: Router )
    {
    }

    loginAttempt$ = createEffect( () =>
        this.actions$.pipe
        (
            ofType( loginAttempt ),
            concatMap( ( { requestLogin } ) =>
                this.authService.loginPost( requestLogin ).pipe(
                    mergeMap( ( csrfPair: TypeCSRFPair ) =>
                        {
                            this.authService.configuration.credentials[ "CSRFAcessToken" ] = csrfPair.csrf_access_token
                            this.router.navigate( [ '/users' ] )
                            return of( loginSuccess( {
                                csrfPair: {
                                    csrf_access_token: csrfPair.csrf_access_token,
                                    csrf_refresh_token: csrfPair.csrf_refresh_token
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
                    mergeMap( ( userInfo: TypeUserInfo ) =>
                        of( registerSuccess( { userInfo: userInfo } ) ) ),
                    catchError(
                        error =>
                            of( loginError( { error: error } ) )
                    )
                )
            )
        )
    )
}