import { Component, Input, OnDestroy, OnInit } from '@angular/core'
import { TaskForUserResponseTaskParticipant } from '@api/tasks/model'
import { Observable, Subscription } from 'rxjs'
import { SafeUrl } from '@angular/platform-browser'
import { ContestAssignmentItemStore } from '@/contests/components/contest-assignment-item/contest-assignment-item.store'


@Component( {
    selector: 'app-contest-assignment-item',
    templateUrl: './contest-assignment-item.component.html',
    styleUrls: [ './contest-assignment-item.component.scss' ],
    providers: [ ContestAssignmentItemStore ]
} )
export class ContestAssignmentItemComponent implements OnInit, OnDestroy
{
    @Input() task!: TaskForUserResponseTaskParticipant
    @Input() taskIndex!: number
    answer!: number
    @Input() contestId!: number | null
    taskImageUrl$: Observable<SafeUrl> = this.contestAssignmentItemStore.taskImageUrl$
    private subscription!: Subscription

    constructor( private contestAssignmentItemStore: ContestAssignmentItemStore )
    {
    }

    ngOnInit(): void
    {
        if ( !!this.contestId )
        {
            const contestTask = { contestId: this.contestId, taskId: this.task.task_id }
            this.contestAssignmentItemStore.fetchTaskImage( contestTask )
            this.contestAssignmentItemStore.fetchAnswer( contestTask )
            this.subscription = this.contestAssignmentItemStore.answer$.subscribe( item =>
            {
                if ( !!item?.answer )
                    this.answer = item?.answer
            } )
        }
    }

    ngOnDestroy(): void
    {
        this.subscription.unsubscribe()
    }

    onSubmit()
    {
        if ( this.contestId )
        {
            const contestTask: { contestId: number, taskId: number, answer: number } = {
                contestId: this.contestId,
                taskId: this.task.task_id,
                answer: this.answer
            }
            this.contestAssignmentItemStore.updateAnswer( contestTask )
        }
    }

    numberOnly( el: HTMLInputElement ): void
    {
        const keyPressed = el.value.split( '' ).pop()
        let transformedKey = keyPressed

        if ( keyPressed === "." )
            transformedKey = "."
        else if ( keyPressed === "-" )
            transformedKey = "-"
        else if ( keyPressed === "," )
            transformedKey = "."
        const newString = el.value.substring( 0, el.value.length - 1 ) + transformedKey
        const pattern: RegExp = /^[-]?([0-9]+\.?[0-9]*|\.[0-9]+)$/
        if ( !pattern.test( newString ) )
            transformedKey = ""
        console.log( newString, transformedKey )
        el.value = el.value.substring( 0, el.value.length - 1 ) + transformedKey
    }
}
