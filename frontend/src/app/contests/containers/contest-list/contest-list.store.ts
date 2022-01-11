import { Injectable } from '@angular/core'
import { ComponentStore, tapResponse } from '@ngrx/component-store'
import { TasksService } from '@api/tasks/tasks.service'
import { CallState, getError, LoadingState } from '@/shared/callState'
import { EMPTY, Observable, of } from 'rxjs'
import {
    EnrollRequestTaskParticipant,
    FilterSimpleContestResponseTaskParticipant,
    OlympiadLocation,
    SimpleContest,
    SimpleContestWithFlagResponseTaskParticipant
} from '@api/tasks/model'
import { catchError, switchMap, tap } from 'rxjs/operators'
import { ResponsesService } from '@api/responses/responses.service'
import { displayErrorMessage } from '@/shared/logging'
import { Router } from '@angular/router'
import CompositeTypeEnum = SimpleContest.CompositeTypeEnum


export interface ContestsState
{
    contests: Array<SimpleContestWithFlagResponseTaskParticipant>
    locations: Array<OlympiadLocation>
    callState: CallState
}


const initialState: ContestsState =
    {
        contests: [],
        locations: [],
        callState: LoadingState.INIT
    }


@Injectable()
export class ContestListStore extends ComponentStore<ContestsState>
{
    constructor( private tasksService: TasksService )
    {
        super( initialState )
    }

    readonly contests$: Observable<SimpleContestWithFlagResponseTaskParticipant[]> = this.select( state => state.contests.filter( item =>
    {
        return item.contest !== undefined
    } ) )
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

    readonly setContests = this.updater( ( state: ContestsState, contests: Array<SimpleContestWithFlagResponseTaskParticipant> ) =>
        ( {
            ...state,
            error: "",
            contests: [ ...state.contests, ...contests ]
        } ) )


    // EFFECTS
    readonly fetchAll = this.effect( ( userGrade$: Observable<number> ) =>
        userGrade$.pipe(
            switchMap( ( userGrade: number ) =>
            {
                return this.tasksService.tasksParticipantOlympiadAllGet( true, undefined, undefined, undefined, undefined, 2021, undefined, undefined, undefined, CompositeTypeEnum.SimpleContest ).pipe(
                    tapResponse(
                        ( response: FilterSimpleContestResponseTaskParticipant ) => this.setContests( response.contest_list?.filter( item => this.filterContest( item, userGrade ) ) ?? [] ),
                        ( error: string ) => this.updateError( error )
                    ),
                    catchError( ( error: any ) => of( displayErrorMessage( error ) ) )
                )
            } ) ) )

    filterContest( item: SimpleContestWithFlagResponseTaskParticipant, userGrade: number )
    {
        if ( item.contest === undefined )
            return false
        if ( item.contest.base_contest.target_classes === undefined )
            return false
        return item.contest.base_contest.target_classes.some( targetClass => targetClass.target_class == userGrade.toString() )
    }



}