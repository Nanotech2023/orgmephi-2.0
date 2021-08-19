import { Injectable } from '@angular/core'
import { ComponentStore, tapResponse } from '@ngrx/component-store'
import { ContestsInStage, ContestsInStageContestsList } from '@/manage-olympiads/api/models'
import { CallState, getError, LoadingState } from '@/shared/callState'
import { EMPTY, Observable } from 'rxjs'
import { catchError, concatMap } from 'rxjs/operators'
import { OlympiadsService } from '@/manage-olympiads/api/olympiads.service'


export interface ManageOlympiadsState
{
    olympiads: Array<ContestsInStageContestsList>
    callState: CallState
}


@Injectable()
export class ManageOlympiadsStore extends ComponentStore<ManageOlympiadsState>
{
    constructor( private olympiadsService: OlympiadsService )
    {
        super( { olympiads: [], callState: LoadingState.INIT } )
    }

    readonly olympiads$: Observable<ContestsInStageContestsList[]> = this.select( state => state.olympiads )
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

    readonly updateUsers = this.updater( ( state: ManageOlympiadsState, olympiad: ContestsInStageContestsList ) =>
        ( {
            ...state,
            error: "",
            olympiads: [ ...state.olympiads, olympiad ]
        } ) )

    // EFFECTS
    readonly reload = this.effect( ( dummy$: Observable<boolean> ) =>
        dummy$.pipe(
            concatMap( ( dummy: boolean ) =>
                {
                    this.setLoading()
                    return this.olympiadsService.olympiadAllGet().pipe(
                        tapResponse(
                            ( response: ContestsInStage ) =>
                                this.setState( {
                                    olympiads: response.contests_list ?? [],
                                    callState: LoadingState.LOADED
                                } ),
                            ( error: string ) => this.updateError( error )
                        ),
                        catchError( () => EMPTY )
                    )
                }
            )
        ) )


    // readonly add = this.effect( ( xxx$: Observable<XXX> ) =>
    //     xxx$.pipe(
    //         concatMap( ( xxx: XXX ) =>
    //         {
    //             this.setLoading()
    //             // TODO wait for new API
    //             return this.olympiadsService.olympiadCreatePost().pipe(
    //                 tapResponse(
    //                     typeUserInfo =>
    //                     {
    //                         this.setLoaded()
    //                         this.updateUsers()
    //                     },
    //                     ( error: string ) => this.updateError( error )
    //                 ),
    //                 catchError( () => EMPTY )
    //             )
    //         } )
    //     ) )
}