import { Component, Input } from '@angular/core'


@Component( {
    selector: 'app-contest-assignment-item',
    templateUrl: './contest-assignment-item.component.html',
    styleUrls: [ './contest-assignment-item.component.scss' ]
} )
export class ContestAssignmentItemComponent
{
    @Input() taskTitle!: string
    @Input() taskId!: number

    taskImage(): string
    {
        return `assets/task${ this.taskId }.png`
    }
}
