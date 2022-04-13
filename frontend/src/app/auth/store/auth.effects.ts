import { Injectable } from '@angular/core'
import { Actions, createEffect, ofType } from '@ngrx/effects'
import { UsersService } from '@api/users/users.service'
import {
    errorCaught,
    getUserInfoRequest,
    getUserInfoSuccess,
    getUserPhotoRequest,
    getUserPhotoSuccess,
    getUserProfileUnfilledRequest,
    getUserProfileUnfilledSuccess,
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
import { EMPTY, of } from 'rxjs'
import { Router } from '@angular/router'
import { CSRFPairUser, SelfUnfilledResponse, User, UserInfo } from '@api/users/models'
import { TasksService } from '@api/tasks/tasks.service'
import { ResponsesService } from '@api/responses/responses.service'
import { displayErrorMessage, displaySuccessMessage } from '@/shared/logging'


// noinspection JSUnusedGlobalSymbols
@Injectable()
export class AuthEffects
{
    constructor( private actions$: Actions, private router: Router, private authService: UsersService, private tasksService: TasksService, private responsesService: ResponsesService )
    {
    }

    readonly loginRequest$ = createEffect( () =>
        this.actions$.pipe
        (
            ofType( loginRequest ),
            concatMap( ( { loginRequestUser } ) =>
                this.authService.userAuthLoginPost( loginRequestUser ).pipe(
                    mergeMap( ( csrfPair: CSRFPairUser ) =>
                        {
                            this.router.navigate( [ '/home' ] )
                            return of( loginSuccess( { csrfPair: csrfPair } ) )
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
            switchMap( () => [ getUserRequest(), getUserInfoRequest(), getUserPhotoRequest(), getUserProfileUnfilledRequest() ] )
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
                            this.router.navigate( [ '/auth' ] )
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

    readonly getUserProfileUnfilledRequest$ = createEffect( () =>
        this.actions$.pipe(
            ofType( getUserProfileUnfilledRequest ),
            concatMap( () =>
                this.authService.userProfileUnfilledGet().pipe(
                    mergeMap( ( response: SelfUnfilledResponse ) => of( getUserProfileUnfilledSuccess( { unfilled: response.unfilled } ) ) ),
                    catchError( error => of( errorCaught( { error: error } ) ) )
                )
            )
        )
    )

    // readonly getUserPhotoRequest$ = createEffect( () =>
    //     this.actions$.pipe(
    //         ofType( getUserPhotoRequest ),
    //         concatMap( () =>
    //             this.authService.userProfilePhotoGet().pipe(
    //                 mergeMap( ( photo: Blob ) => of( getUserPhotoSuccess( { userPhoto: photo } ) ) ),
    //                 catchError( error => EMPTY )
    //             )
    //         )
    //     )
    // )

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
    readonly registerSuccess$ = createEffect( () =>
            this.actions$.pipe
            (
                ofType( registerSuccess ),
                tap( ( { type } ) => displaySuccessMessage( "Пользователь успешно зарегистрирован" ) ),
                tap( () => this.router.navigate( [ '/auth' ] ) )
            ),
        { dispatch: false }
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