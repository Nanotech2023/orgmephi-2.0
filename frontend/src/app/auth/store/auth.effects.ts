import { Injectable } from '@angular/core'
import { Actions, createEffect, ofType } from '@ngrx/effects'
import { UsersService } from '@api/users/users.service'
import {
    errorCaught,
    getUserRequest,
    getUserSuccess,
    loginRequest,
    loginSuccess,
    registerRequest,
    registerSuccess
} from '@/auth/store/auth.actions'
import { catchError, concatMap, mergeMap, switchMap } from 'rxjs/operators'
import { of } from 'rxjs'
import { Router } from '@angular/router'
import { CSRFPairUser, User } from '@api/users/models'
import { TasksService } from '@api/tasks/tasks.service'
import { ResponsesService } from '@api/responses/responses.service'


// noinspection JSUnusedGlobalSymbols
@Injectable()
export class AuthEffects
{
    constructor( private actions$: Actions, private router: Router, private authService: UsersService, private tasksService: TasksService, private responsesService: ResponsesService )
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

    loginSuccess$ = createEffect( () =>
        this.actions$.pipe(
            ofType( loginSuccess ),
            switchMap( () => [ getUserRequest() ] )
        )
    )


    getUserRequest$ = createEffect( () =>
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

    registerRequest$ = createEffect( () =>
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
}