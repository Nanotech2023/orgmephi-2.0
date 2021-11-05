import { Component, OnInit, ViewChild } from '@angular/core'
import { TasksService } from '@api/tasks/tasks.service'
import { BaseContest } from '@api/tasks/model'
import { DxDataGridComponent } from 'devextreme-angular'
import { ActivatedRoute, Router } from '@angular/router'


@Component( {
    selector: 'app-manage-base-contests',
    templateUrl: './manage-base-contests.component.html',
    styleUrls: [ './manage-base-contests.component.scss' ]
} )
export class ManageBaseContestsComponent implements OnInit
{
    constructor( private router: Router, private route: ActivatedRoute, private tasksService: TasksService ) { }

    ngOnInit(): void
    {
        this.tasksService.tasksUnauthorizedBaseOlympiadAllGet().subscribe( response =>
        {
            this.baseContests = response.olympiad_list
        } )
    }

    baseContests: Array<BaseContest> = []

    @ViewChild( DxDataGridComponent, { static: false } ) grid!: DxDataGridComponent
    selectedRowIndex: number = -1
    selectedRow?: BaseContest = undefined

    navigateElement(): void
    {
        if ( this.selectedRow )
            this.router.navigate( [ this.selectedRow.base_contest_id ], { relativeTo: this.route } )
    }

    editElement(): void
    {
        this.grid.instance.editRow( this.selectedRowIndex )
        this.grid.instance.deselectAll()
    }

    deleteElement(): void
    {
        this.grid.instance.deleteRow( this.selectedRowIndex )
        this.grid.instance.deselectAll()
    }

    addElement(): void
    {
        this.grid.instance.addRow()
        this.grid.instance.deselectAll()
    }

    selectedChanged( $event: any ): void
    {
        this.selectedRow = $event.selectedRowsData[ 0 ]
        this.selectedRowIndex = $event.component.getRowIndexByKey( $event.selectedRowKeys[ 0 ] )
    }
}
