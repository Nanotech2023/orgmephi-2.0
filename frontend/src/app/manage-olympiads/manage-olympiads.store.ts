import { Injectable } from '@angular/core'
import { ComponentStore, tapResponse } from '@ngrx/component-store'
import { CallState, getError, LoadingState } from '@/shared/callState'
import { EMPTY, Observable } from 'rxjs'
import { catchError, concatMap } from 'rxjs/operators'
import { AllOlympiadsResponseTaskUnauthorized, Contest, CreateBaseOlympiadRequestTaskCreator } from '@api/tasks/model'
import { TasksService } from '@api/tasks/tasks.service'


export interface ManageOlympiadsState
{
    contests: Array<Contest>
    callState: CallState
}


@Injectable()
export class ManageOlympiadsStore extends ComponentStore<ManageOlympiadsState>
{
    constructor( private olympiadsService: TasksService )
    {
        super( { contests: [], callState: LoadingState.INIT } )
    }

    readonly contests: Observable<Contest[]> = this.select( state => state.contests )
    private readonly loading$: Observable<boolean> = this.select( state => state.callState === LoadingState.LOADING )
    private readonly error$: Observable<string | null> = this.select( state => getError( state.callState ) )


    // UPDATERS
    readonly updateError = this.updater( ( state: ManageOlympiadsState, error: string ) =>
        ( {
            ...state,
            callState: { errorMessage: error }
        } ) )

    readonly setLoading = this.updater( ( state: ManageOlympiadsState ) =>
        ( {
            ...state,
            callState: LoadingState.LOADING
        } ) )

    readonly setLoaded = this.updater( ( state: ManageOlympiadsState ) =>
        ( {
            ...state,
            callState: LoadingState.LOADED
        } ) )

    readonly updateContests = this.updater( ( state: ManageOlympiadsState, contests: AllOlympiadsResponseTaskUnauthorized ) =>
        ( {
            ...state,
            error: "",
            contests: [ ...state.contests, ...contests.contest_list ]
        } ) )

    // EFFECTS
    readonly reload = this.effect( () =>
    {
        this.setLoading()
        return this.olympiadsService.tasksParticipantOlympiadAllGet().pipe(
            tapResponse(
                ( response: AllOlympiadsResponseTaskUnauthorized ) =>
                    this.setState( {
                        contests: response.contest_list ?? [],
                        callState: LoadingState.LOADED
                    } ),
                ( error: string ) => this.updateError( error )
            ),
            catchError( () => EMPTY )
        )
    } )


    readonly add = this.effect( ( olympiadRequestTaskCreatorObservable: Observable<CreateBaseOlympiadRequestTaskCreator> ) =>
        olympiadRequestTaskCreatorObservable.pipe(
            concatMap( ( xxx: CreateBaseOlympiadRequestTaskCreator ) =>
            {
                this.setLoading()
                return this.olympiadsService.tasksCreatorBaseOlympiadCreatePost(xxx).pipe(
                    tapResponse(
                        () =>
                        {
                            this.setLoaded()
                            this.reload()
                        },
                        ( error: string ) => this.updateError( error )
                    ),
                    catchError( () => EMPTY )
                )
            } )
        ) )
}