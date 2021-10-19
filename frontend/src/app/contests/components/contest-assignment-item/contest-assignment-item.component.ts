import { Component, EventEmitter, Input, OnDestroy, OnInit, Output } from '@angular/core'
import { TaskForUserResponseTaskParticipant } from '@api/tasks/model'
import { ResponsesService } from '@api/responses/responses.service'
import { TasksService } from '@api/tasks/tasks.service'
import { Subscription } from 'rxjs'
import { DomSanitizer, SafeUrl } from '@angular/platform-browser'
import { PlainAnswerRequest } from '@api/responses/model'


@Component( {
    selector: 'app-contest-assignment-item',
    templateUrl: './contest-assignment-item.component.html',
    styleUrls: [ './contest-assignment-item.component.scss' ]
} )
export class ContestAssignmentItemComponent implements OnInit, OnDestroy
{
    @Input() task!: TaskForUserResponseTaskParticipant
    @Input() contestId!: number | null
    imageUrl!: SafeUrl
    private subscription!: Subscription
    @Output() answered: EventEmitter<boolean> = new EventEmitter<boolean>()
    answer: string = ""

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
            let plainAnswerRequest: PlainAnswerRequest = { answer_text: this.answer }
            this.responsesService.responsesParticipantContestContestIdTaskTaskIdUserSelfPlainPost( this.contestId as number, this.task.task_id, plainAnswerRequest ).subscribe()
            this.answered.emit( true )
        }
    }
}
