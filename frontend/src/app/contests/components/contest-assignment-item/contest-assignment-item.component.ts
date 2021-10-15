import { Component, Input, OnDestroy, OnInit } from '@angular/core'
import { TaskForUserResponseTaskParticipant } from '@api/tasks/model'
import { ResponsesService } from '@api/responses/responses.service'
import { TasksService } from '@api/tasks/tasks.service'
import { Observable, Subscription } from 'rxjs'
import { DomSanitizer, SafeUrl } from '@angular/platform-browser'


@Component( {
    selector: 'app-contest-assignment-item',
    templateUrl: './contest-assignment-item.component.html',
    styleUrls: [ './contest-assignment-item.component.scss' ]
} )
export class ContestAssignmentItemComponent implements OnInit, OnDestroy
{
    @Input() task!: TaskForUserResponseTaskParticipant
    @Input() contestId!: number | null
    taskImage!: Observable<Blob>
    imageUrl!: SafeUrl
    private subscription!: Subscription

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
}
