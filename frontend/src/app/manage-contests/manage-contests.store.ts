import { Injectable } from '@angular/core'
import { ComponentStore, tapResponse } from '@ngrx/component-store'
import { CallState, getError, LoadingState } from '@/shared/callState'
import { EMPTY, Observable } from 'rxjs'
import { catchError } from 'rxjs/operators'
import {
    FilterSimpleContestResponseTaskParticipant,
    SimpleContestWithFlagResponseTaskParticipant
} from '@api/tasks/model'
import { TasksService } from '@api/tasks/tasks.service'


export interface ManageContestsState
{
    contests: Array<SimpleContestWithFlagResponseTaskParticipant>
    callState: CallState
}


const initialState = {
    contests: [],
    callState: LoadingState.INIT
}


@Injectable()
export class ManageContestsStore extends ComponentStore<ManageContestsState>
{
    constructor( private tasksService: TasksService )
    {
        super( initialState )
    }

    readonly contests$: Observable<SimpleContestWithFlagResponseTaskParticipant[]> = this.select( state => state.contests )
    private readonly loading$: Observable<boolean> = this.select( state => state.callState === LoadingState.LOADING )
    private readonly error$: Observable<string | null> = this.select( state => getError( state.callState ) )


    // UPDATERS
    readonly updateError = this.updater( ( state: ManageContestsState, error: string ) =>
        ( {
            ...state,
            callState: { errorMessage: error }
        } ) )

    readonly setLoading = this.updater( ( state: ManageContestsState ) =>
        ( {
            ...state,
            callState: LoadingState.LOADING
        } ) )

    readonly setLoaded = this.updater( ( state: ManageContestsState ) =>
        ( {
            ...state,
            callState: LoadingState.LOADED
        } ) )


    // EFFECTS
    readonly reload = this.effect( () =>
    {
        this.setLoading()
        return this.tasksService.tasksParticipantOlympiadAllGet().pipe(
            tapResponse(
                ( response: FilterSimpleContestResponseTaskParticipant ) =>
                    this.setState( {
                        contests: response.contest_list ?? [],
                        callState: LoadingState.LOADED
                    } ),
                ( error: string ) => this.updateError( error )
            ),
            catchError( () => EMPTY )
        )
    } )
}