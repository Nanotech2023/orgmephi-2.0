import { Component, Input } from '@angular/core'
import { TargetClass } from '@api/tasks/model'


@Component( {
    selector: 'app-manage-target-classes',
    templateUrl: './manage-target-classes.component.html',
    styleUrls: [ './manage-target-classes.component.scss' ],
} )
export class ManageTargetClassesComponent
{
    @Input() rowData!: Array<TargetClass>
}
