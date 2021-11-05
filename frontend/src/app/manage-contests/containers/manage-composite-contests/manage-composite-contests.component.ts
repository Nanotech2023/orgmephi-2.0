import { Component, OnInit, ViewChild } from '@angular/core'
import { ActivatedRoute, Router } from '@angular/router'
import { TasksService } from '@api/tasks/tasks.service'
import { BaseContest, CompositeContest } from '@api/tasks/model'
import CompositeTypeEnum = CompositeContest.CompositeTypeEnum
import { DxDataGridComponent } from 'devextreme-angular'


@Component( {
    selector: 'app-manage-composite-contests',
    templateUrl: './manage-composite-contests.component.html',
    styleUrls: [ './manage-composite-contests.component.scss' ]
} )
export class ManageCompositeContestsComponent
{
    constructor( private route: ActivatedRoute, private router: Router, private tasksService: TasksService )
    {
        this.route.paramMap.subscribe( paramMap =>
        {
            this.baseContestId = Number( paramMap.get( 'baseContestId' ) )
            if ( !!this.baseContestId )
            {
                this.tasksService.tasksUnauthorizedOlympiadAllGet( undefined, undefined, this.baseContestId, undefined, undefined, undefined, undefined, undefined, CompositeTypeEnum.CompositeContest ).subscribe( response =>
                {
                    this.compositeContests = response.contest_list! as CompositeContest[]
                } )
            }
        } )
    }

    baseContestId!: number
    compositeContests: Array<CompositeContest> = []

    @ViewChild( DxDataGridComponent, { static: false } ) grid!: DxDataGridComponent
    selectedRowIndex: number = -1
    selectedRow?: CompositeContest = undefined

    navigateElement(): void
    {
        if ( this.selectedRow )
            this.router.navigate( [ 'composite', this.selectedRow.contest_id, 'stages' ], { relativeTo: this.route } )
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
