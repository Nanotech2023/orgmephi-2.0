import { Component, OnInit, ViewChild } from '@angular/core'
import { ManageContestsStore } from '@/manage-contests/manage-contests.store'
import { Observable } from 'rxjs'
import { SimpleContestWithFlagResponseTaskParticipant } from '@api/tasks/model'
import { TasksService } from '@api/tasks/tasks.service'
import { DxDataGridComponent } from 'devextreme-angular'


@Component( {
    selector: 'app-manage-contests',
    templateUrl: './manage-contests.component.html',
    styleUrls: [ './manage-contests.component.scss' ],
    providers: [ ManageContestsStore ]
} )
export class ManageContestsComponent implements OnInit
{
    @ViewChild( DxDataGridComponent, { static: false } ) grid!: DxDataGridComponent
    contests$: Observable<SimpleContestWithFlagResponseTaskParticipant[]> = this.store.contests$
    selectedRowIndex = -1

    constructor( private store: ManageContestsStore, private tasksService: TasksService ) {}

    ngOnInit(): void
    {
        //this.tasksService.tasksCreatorCreatePost
        this.store.reload()
    }

    editRow(): void
    {
        this.grid.instance.editRow( this.selectedRowIndex )
        this.grid.instance.deselectAll()
    }

    deleteRow(): void
    {
        this.grid.instance.deleteRow( this.selectedRowIndex )
        this.grid.instance.deselectAll()
    }

    addRow(): void
    {
        this.grid.instance.addRow()
        this.grid.instance.deselectAll()
    }

    selectedChanged( e: any ): void
    {
        this.selectedRowIndex = e.component.getRowIndexByKey( e.selectedRowKeys[ 0 ] )
    }
}
