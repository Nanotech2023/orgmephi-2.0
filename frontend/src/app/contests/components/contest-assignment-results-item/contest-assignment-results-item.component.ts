import { Component, Input, OnInit } from '@angular/core'
import { DomSanitizer, SafeUrl } from '@angular/platform-browser'
import { Subscription } from 'rxjs'
import { TasksService } from '@api/tasks/tasks.service'
import { ResponsesService } from '@api/responses/responses.service'
import { BaseAnswer, RangeAnswer, RangeRightAnswer, TaskForUserResponseResults } from '@api/responses/model'


@Component( {
    selector: 'app-contest-assignment-results-item',
    templateUrl: './contest-assignment-results-item.component.html',
    styleUrls: [ './contest-assignment-results-item.component.scss' ]
} )
export class ContestAssignmentResultsItemComponent implements OnInit
{
    @Input() task!: TaskForUserResponseResults
    @Input() taskIndex!: number
    @Input() answer!: BaseAnswer | undefined
    @Input() contestId!: number | null
    imageUrl!: SafeUrl
    private subscription!: Subscription
    userAnswer!: number | undefined

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
            this.responsesService.responsesParticipantContestContestIdTaskTaskIdUserSelfGet( this.contestId, this.task.task_id ).subscribe( item => this.userAnswer = ( item as RangeAnswer )?.answer ?? undefined )
        }
    }

    ngOnDestroy(): void
    {
        this.subscription?.unsubscribe()
    }
}