import { Injectable } from '@angular/core'
import { Actions, createEffect, ofType } from '@ngrx/effects'
import { UsersService } from '@api/users/users.service'
import {
    errorCaught,
    getUserInfoRequest,
    getUserInfoSuccess, getUserPhotoRequest, getUserPhotoSuccess,
    getUserRequest,
    getUserSuccess,
    loginRequest,
    loginSuccess,
    logoutRequest,
    logoutSuccess,
    registerRequest,
    registerSuccess
} from '@/auth/store/auth.actions'
import { catchError, concatMap, mergeMap, switchMap, tap } from 'rxjs/operators'
import { of } from 'rxjs'
import { Router } from '@angular/router'
import { CSRFPairUser, User, UserInfo } from '@api/users/models'
import { TasksService } from '@api/tasks/tasks.service'
import { ResponsesService } from '@api/responses/responses.service'
import { displayErrorMessage } from '@/shared/logging'


// noinspection JSUnusedGlobalSymbols
@Injectable()
export class AuthEffects
{
    constructor( private actions$: Actions, private router: Router, private authService: UsersService, private tasksService: TasksService, private responsesService: ResponsesService )
    {
    }

    readonly loginAttempt$ = createEffect( () =>
        this.actions$.pipe
        (
            ofType( loginRequest ),
            concatMap( ( { loginRequestUser } ) =>
                this.authService.userAuthLoginPost( loginRequestUser ).pipe(
                    mergeMap( ( csrfPair: CSRFPairUser ) =>
                        {
                            this.router.navigate( [ '/home' ] )
                            return of( loginSuccess( {
                                csrfPair: csrfPair
                            } ) )
                        }
                    ),
                    catchError( error => of( errorCaught( { error: error } ) ) )
                )
            )
        )
    )

    readonly loginSuccess$ = createEffect( () =>
        this.actions$.pipe(
            ofType( loginSuccess ),
            switchMap( () => [ getUserRequest(), getUserInfoRequest(), getUserPhotoRequest() ] )
        )
    )

    readonly logoutRequest$ = createEffect( () =>
        this.actions$.pipe
        (
            ofType( logoutRequest ),
            concatMap( () =>
                this.authService.userAuthLogoutPost().pipe(
                    mergeMap( () =>
                        {
                            this.router.navigate( [ '/login' ] )
                            return of( logoutSuccess() )
                        }
                    ),
                    catchError( error => of( errorCaught( { error: error } ) ) )
                )
            )
        )
    )

    readonly getUserRequest$ = createEffect( () =>
        this.actions$.pipe(
            ofType( getUserRequest ),
            concatMap( () =>
                this.authService.userProfileUserGet().pipe(
                    mergeMap( ( user: User ) => of( getUserSuccess( { user: user } ) ) ),
                    catchError( error => of( errorCaught( { error: error } ) ) )
                )
            )
        )
    )

    readonly getUserInfoRequest$ = createEffect( () =>
        this.actions$.pipe(
            ofType( getUserInfoRequest ),
            concatMap( () =>
                this.authService.userProfilePersonalGet().pipe(
                    mergeMap( ( userInfo: UserInfo ) => of( getUserInfoSuccess( { userInfo: userInfo } ) ) ),
                    catchError( error => of( errorCaught( { error: error } ) ) )
                )
            )
        )
    )

    readonly getUserPhotoRequest$ = createEffect( () =>
        this.actions$.pipe(
            ofType( getUserPhotoRequest ),
            concatMap( () =>
                this.authService.userProfilePhotoGet().pipe(
                    mergeMap( ( photo: Blob ) => of( getUserPhotoSuccess( { userPhoto: photo } ) ) ),
                    catchError( error => of( errorCaught( { error: error } ) ) )
                )
            )
        )
    )

    readonly registerRequest$ = createEffect( () =>
        this.actions$.pipe
        (
            ofType( registerRequest ),
            concatMap( ( { registrationRequestUser } ) =>
                this.authService.userRegistrationSchoolPost( registrationRequestUser ).pipe(
                    mergeMap( () => of( registerSuccess() ) ),
                    catchError( error => of( errorCaught( { error: error } ) )
                    )
                )
            )
        )
    )

    readonly errorCaught$ = createEffect( () =>
            this.actions$.pipe
            (
                ofType( errorCaught ),
                tap( ( { error } ) => displayErrorMessage( error ) )
            ),
        { dispatch: false }
    )
}