import { Injectable } from '@angular/core'
import { ComponentStore, tapResponse } from '@ngrx/component-store'
import { TasksService } from '@api/tasks/tasks.service'
import { CallState, getError, LoadingState } from '@/shared/callState'
import { EMPTY, Observable } from 'rxjs'
import { AllOlympiadsResponseTaskUnauthorized, Contest } from '@api/tasks/model'
import { catchError } from 'rxjs/operators'


export interface ContestsState
{
    contests: Array<Contest>
    callState: CallState
    selectedId: number | null
    selectedEntity?: Contest
}


const initialState: ContestsState = {
    callState: LoadingState.INIT,
    contests: [],
    selectedId: null,
    selectedEntity: undefined
}


@Injectable()
export class ContestsStore extends ComponentStore<ContestsState>
{
    constructor( private tasksService: TasksService )
    {
        super( initialState )
    }

    readonly contests: Observable<Contest[]> = this.select( state => state.contests )
    private readonly loading$: Observable<boolean> = this.select( state => state.callState === LoadingState.LOADING )
    private readonly error$: Observable<string | null> = this.select( state => getError( state.callState ) )


    // UPDATERS
    readonly updateError = this.updater( ( state: ContestsState, error: string ) =>
        ( {
            ...state,
            callState: { errorMessage: error }
        } ) )

    readonly setLoading = this.updater( ( state: ContestsState ) =>
        ( {
            ...state,
            callState: LoadingState.LOADING
        } ) )

    readonly setLoaded = this.updater( ( state: ContestsState ) =>
        ( {
            ...state,
            callState: LoadingState.LOADED
        } ) )

    readonly updateContests = this.updater( ( state: ContestsState, contests: Array<Contest> ) =>
        ( {
            ...state,
            error: "",
            contests: [ ...state.contests, ...contests ]
        } ) )

    readonly details = this.updater( ( state: ContestsState, id: number ) =>
        ( {
            ...state,
            selectedId: id,
            selectedEntity: state.contests.find( item => item.contest_id === id )
        } ) )

    // EFFECTS
    readonly reload = this.effect( () =>
    {
        this.setLoading()
        return this.tasksService.tasksParticipantOlympiadAllGet().pipe(
            tapResponse(
                ( response: AllOlympiadsResponseTaskUnauthorized ) => this.updateContests( response.contest_list ),
                ( error: string ) => this.updateError( error )
            ),
            catchError( () => EMPTY )
        )
    } )
}