import { Actions, createEffect, ofType, ROOT_EFFECTS_INIT } from '@ngrx/effects'
import { catchError, concatMap, finalize, mergeMap } from 'rxjs/operators'
import { CSRFPairUser } from '@api/users/models'
import { of } from 'rxjs'
import { errorCaught, loginSuccess } from '@/auth/store/auth.actions'
import { Injectable } from '@angular/core'
import { Router } from '@angular/router'
import { UsersService } from '@api/users/users.service'
import { TasksService } from '@api/tasks/tasks.service'
import { ResponsesService } from '@api/responses/responses.service'


// noinspection JSUnusedGlobalSymbols
@Injectable()
export class RootEffects
{
    constructor( private actions$: Actions, private router: Router, private authService: UsersService, private tasksService: TasksService, private responsesService: ResponsesService )
    {
    }


    readonly init$ = createEffect( () =>
        this.actions$.pipe(
            ofType( ROOT_EFFECTS_INIT ),
            concatMap( () => this.authService.userAuthRefreshPost().pipe(
                mergeMap( ( csrfPair: CSRFPairUser ) =>
                    of( loginSuccess( { csrfPair } ) )
                ),
                finalize( () => this.router.initialNavigation() ),
                catchError( error => of( errorCaught( { error: error } ) ) )
            ) )
        ) )
}