import { Component, Input, OnDestroy, OnInit } from '@angular/core'
import { TaskForUserResponseTaskParticipant } from '@api/tasks/model'
import { ResponsesService } from '@api/responses/responses.service'
import { TasksService } from '@api/tasks/tasks.service'
import { Subscription } from 'rxjs'
import { DomSanitizer, SafeUrl } from '@angular/platform-browser'
import { RangeAnswer, RangeAnswerRequest } from '@api/responses/model'


@Component( {
    selector: 'app-contest-assignment-item',
    templateUrl: './contest-assignment-item.component.html',
    styleUrls: [ './contest-assignment-item.component.scss' ]
} )
export class ContestAssignmentItemComponent implements OnInit, OnDestroy
{
    @Input() task!: TaskForUserResponseTaskParticipant
    @Input() taskIndex!: number
    @Input() contestId!: number | null
    imageUrl!: SafeUrl
    private subscription!: Subscription
    answer!: number | undefined

    constructor( private tasksService: TasksService, private responsesService: ResponsesService, private sanitizer: DomSanitizer )
    {
    }

    ngOnInit(): void
    {
        if ( !!this.contestId )
        {
            this.subscription = this.tasksService.tasksParticipantContestIdContestTasksIdTaskImageSelfGet( this.contestId, this.task.task_id ).subscribe( data =>
            {
                const unsafeImageUrl = URL.createObjectURL( data )
                this.imageUrl = this.sanitizer.bypassSecurityTrustUrl( unsafeImageUrl )
            } )
            this.responsesService.responsesParticipantContestContestIdTaskTaskIdUserSelfGet( this.contestId, this.task.task_id ).subscribe( item => this.answer = ( item as RangeAnswer )?.answer ?? undefined )
        }
    }

    ngOnDestroy(): void
    {
        this.subscription?.unsubscribe()
    }

    updateAnswer()
    {
        if ( this.answer )
        {
            const rangeAnswerRequest: RangeAnswerRequest = { answer: this.answer }
            this.responsesService.responsesParticipantContestContestIdTaskTaskIdUserSelfRangePost( this.contestId as number, this.task.task_id, rangeAnswerRequest ).subscribe()
        }
    }

    numberOnly( el: HTMLInputElement ): void
    {
        const keyPressed = el.value.split( '' ).pop()
        let transformedKey = keyPressed

        if ( keyPressed === "," )
            transformedKey = "."

        if ( isNaN( Number( keyPressed ) ) )
            transformedKey = ""

        const newString = el.value.substring( 0, el.value.length - 1 ) + transformedKey
        el.value = newString
        this.updateAnswer()
    }
}
