import { Injectable } from '@angular/core'
import { ComponentStore, tapResponse } from '@ngrx/component-store'
import { ResponsesService } from '@api/responses/responses.service'
import { CallState, getError, LoadingState } from '@/shared/callState'
import { EMPTY, Observable } from 'rxjs'
import { catchError } from 'rxjs/operators'
import { AllUserResultsResponse, UserResultsForContestResponse } from '@api/responses/model'


export interface ContestResultsState
{
    callState: CallState,
    results: UserResultsForContestResponse[]
}


const initialState: ContestResultsState = {
    callState: LoadingState.INIT,
    results: []
}


@Injectable()
export class ContestResultsStore extends ComponentStore<ContestResultsState>
{
    constructor( private responsesService: ResponsesService )
    {
        super( initialState )
    }

    private readonly loading$: Observable<boolean> = this.select( state => state.callState === LoadingState.LOADING )
    private readonly error$: Observable<string | null> = this.select( state => getError( state.callState ) )
    readonly results$: Observable<UserResultsForContestResponse[]> = this.select( state => state.results )


    // UPDATERS
    readonly updateError = this.updater( ( state: ContestResultsState, error: string ) =>
        ( {
            ...state,
            callState: { errorMessage: error }
        } ) )

    readonly setLoading = this.updater( ( state: ContestResultsState ) =>
        ( {
            ...state,
            callState: LoadingState.LOADING
        } ) )

    readonly setLoaded = this.updater( ( state: ContestResultsState ) =>
        ( {
            ...state,
            callState: LoadingState.LOADED
        } ) )

    readonly setResults = this.updater( ( state: ContestResultsState, results: UserResultsForContestResponse[] ) =>
        ( {
            ...state,
            results: results
        } ) )

    // EFFECTS
    readonly fetchAll = this.effect( () =>
    {
        this.setLoading()
        return this.responsesService.responsesParticipantContestUserSelfResultsGet().pipe(
            tapResponse(
                ( response: AllUserResultsResponse ) => this.setResults( response.results ?? [] ),
                ( error: string ) => this.updateError( error )
            ),
            catchError( () => EMPTY )
        )
    } )
}
