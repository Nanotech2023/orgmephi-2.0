import { Injectable } from '@angular/core'
import { Actions, createEffect, ofType } from '@ngrx/effects'
import { AuthService } from '@/auth/api/auth.service'
import {
    getUserInfoRequest,
    getUserInfoSuccess, getUserSuccess,
    loginRequest,
    loginSuccess,
    registerRequest,
    registerSuccess
} from '@/auth/store/auth.actions'
import { catchError, concatMap, mergeMap, switchMap } from 'rxjs/operators'
import { of } from 'rxjs'
import { Router } from '@angular/router'
import { CSRFPairUser, User, UserInfo } from '@/auth/api/models'


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
            concatMap( ( { loginRequestUser } ) =>
                this.authService.userAuthLoginPost( loginRequestUser ).pipe(
                    mergeMap( ( csrfPair: CSRFPairUser ) =>
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
            switchMap( () => [ getUserInfoRequest() ] )
        )
    )


    getUserRequest$ = createEffect( () =>
        this.actions$.pipe(
            ofType( getUserInfoRequest ),
            concatMap( () =>
                this.authService.userProfileUserGet().pipe(
                    mergeMap( ( user: User ) => of( getUserSuccess( { user: user } ) ) ),
                    catchError( error => of( error( { error: error } ) ) )
                )
            )
        )
    )

    getUserInfoRequest$ = createEffect( () =>
        this.actions$.pipe(
            ofType( getUserInfoRequest ),
            concatMap( () =>
                this.authService.userProfilePersonalGet().pipe(
                    mergeMap( ( userInfo: UserInfo ) => of( getUserInfoSuccess( { userInfo: userInfo } ) ) ),
                    catchError( error => of( error( { error: error } ) ) )
                )
            )
        )
    )


    registerAttempt$ = createEffect( () =>
        this.actions$.pipe
        (
            ofType( registerRequest ),
            concatMap( ( { registrationRequestUser } ) =>
                this.authService.userRegistrationSchoolPost( registrationRequestUser ).pipe(
                    mergeMap( () => of( registerSuccess() ) ),
                    catchError( error => of( error( { error: error } ) )
                    )
                )
            )
        )
    )
}