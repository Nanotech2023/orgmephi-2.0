import { Injectable } from '@angular/core'
import { ComponentStore, tapResponse } from '@ngrx/component-store'
import { TasksService } from '@api/tasks/tasks.service'
import { DomSanitizer, SafeUrl } from '@angular/platform-browser'
import { Observable, of } from 'rxjs'
import { ResponsesService } from '@api/responses/responses.service'
import { catchError, switchMap, withLatestFrom } from 'rxjs/operators'
import { displayErrorMessage } from '@/shared/logging'
import { RangeAnswer, RangeAnswerRequest, UserAnswer } from '@api/responses/model'


export interface ContestAssignmentItemState
{
    taskImageUrl?: SafeUrl,
    answer?: RangeAnswer
}


const initialState: ContestAssignmentItemState = {
    taskImageUrl: undefined,
    answer: undefined
}


@Injectable()
export class ContestAssignmentItemStore extends ComponentStore<ContestAssignmentItemState>
{
    constructor( private tasksService: TasksService, private responsesService: ResponsesService, private sanitizer: DomSanitizer )
    {
        super( initialState )
    }

    readonly answer$: Observable<RangeAnswer | undefined> = this.select( state => state.answer )
    readonly taskImageUrl$: Observable<SafeUrl> = this.select( state => state.taskImageUrl! )

    // UPDATERS
    readonly setTaskImage = this.updater( ( state: ContestAssignmentItemState, response: Blob ) =>
        ( {
            ...state,
            taskImageUrl: this.sanitizer.bypassSecurityTrustUrl( URL.createObjectURL( response ) )
        } ) )

    readonly setUserAnswer = this.updater( ( state: ContestAssignmentItemState, response: UserAnswer ) =>
        ( {
            ...state,
            answer: response as RangeAnswer
        } ) )

    // EFFECTS
    readonly fetchTaskImage = this.effect( ( contestTask$: Observable<{ contestId: number, taskId: number }> ) =>
        contestTask$.pipe(
            switchMap( ( contestTask: { contestId: number; taskId: number } ) =>
                this.tasksService.tasksParticipantContestIdContestTasksIdTaskImageSelfGet( contestTask.contestId, contestTask.taskId ).pipe(
                    tapResponse(
                        ( response: Blob ) => this.setTaskImage( response ),
                        ( ( _ ) => {} )
                    ) ) )
        ) )

    readonly fetchAnswer = this.effect( ( contestTask$: Observable<{ contestId: number, taskId: number }> ) =>
        contestTask$.pipe(
            switchMap( ( contestTask: { contestId: number; taskId: number } ) =>
                this.responsesService.responsesParticipantContestContestIdTaskTaskIdUserSelfGet( contestTask.contestId, contestTask.taskId ).pipe(
                    tapResponse(
                        ( response: UserAnswer ) => this.setUserAnswer( response ),
                        ( ( _ ) => {} )
                    ) ) )
        ) )

    readonly updateAnswer = this.effect( ( contestTaskAnswer$: Observable<{ contestId: number, taskId: number, answer: number }> ) =>
        contestTaskAnswer$.pipe(
            switchMap( ( contestTaskAnswer: { contestId: number; taskId: number; answer: number } ) =>
            {
                const answerRequest: RangeAnswerRequest = { answer: contestTaskAnswer.answer }
                return this.responsesService.responsesParticipantContestContestIdTaskTaskIdUserSelfRangePost( contestTaskAnswer.contestId, contestTaskAnswer.taskId, answerRequest ).pipe(
                    catchError( ( error: any ) => of( displayErrorMessage( error ) ) ) )
            } )
        ) )
}
