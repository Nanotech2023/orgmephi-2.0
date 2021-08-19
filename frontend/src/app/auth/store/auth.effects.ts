import { Injectable } from '@angular/core'
import { Actions, createEffect, ofType } from '@ngrx/effects'
import { AuthService } from '@/auth/api/auth.service'
import {
    getPersonalInfoRequest,
    getPersonalInfoSuccess,
    getUserInfoRequest,
    getUserInfoSuccess,
    loginRequest,
    loginSuccess,
    registerRequest,
    registerSuccess
} from '@/auth/store/auth.actions'
import { catchError, concatMap, mergeMap, switchMap } from 'rxjs/operators'
import { of } from 'rxjs'
import { TypeCSRFPair, TypePersonalInfo, TypeUserInfo } from '@/auth/api/models'
import { Router } from '@angular/router'


// noinspection JSUnusedGlobalSymbols
@Injectable()
export class AuthEffects
{
    constructor( private actions$: Actions, private authService: AuthService, private router: Router )
    {
    }

    loginAttempt$ = createEffect( () =>
        this.actions$.pipe
        (
            ofType( loginRequest ),
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
                    catchError( error => of( error( { error: error } ) ) )
                )
            )
        )
    )

    loginSuccess$ = createEffect( () =>
        this.actions$.pipe(
            ofType( loginSuccess ),
            switchMap( () => [ getPersonalInfoRequest(), getUserInfoRequest() ] )
        )
    )

    getUserInfoRequest$ = createEffect( () =>
        this.actions$.pipe(
            ofType( getUserInfoRequest ),
            concatMap( () =>
                this.authService.userSelfGet().pipe(
                    mergeMap( ( userInfo: TypeUserInfo ) =>
                        of( getUserInfoSuccess( { userInfo: userInfo } ) )
                    ),
                    catchError( error => of( error( { error: error } ) ) )
                )
            )
        )
    )

    getPersonalInfoRequest$ = createEffect( () =>
        this.actions$.pipe(
            ofType( getPersonalInfoRequest ),
            concatMap( () =>
                this.authService.userSelfPersonalGet().pipe(
                    mergeMap( ( personalInfo: TypePersonalInfo ) =>
                        of( getPersonalInfoSuccess( { personalInfo: personalInfo } ) )
                    ),
                    catchError( error => of( error( { error: error } ) ) )
                )
            )
        )
    )

    registerAttempt$ = createEffect( () =>
        this.actions$.pipe
        (
            ofType( registerRequest ),
            concatMap( ( { requestRegistration } ) =>
                this.authService.registerSchoolPost( requestRegistration ).pipe(
                    mergeMap( ( userInfo: TypeUserInfo ) =>
                        of( registerSuccess( { userInfo: userInfo } ) ) ),
                    catchError(
                        error =>
                            of( error( { error: error } ) )
                    )
                )
            )
        )
    )
}