import { Component, OnInit, ViewChild } from '@angular/core'
import { ActivatedRoute, Router } from '@angular/router'
import { TasksService } from '@api/tasks/tasks.service'
import { CompositeContest, SimpleContest, Stage } from '@api/tasks/model'
import { DxDataGridComponent } from 'devextreme-angular'


@Component( {
    selector: 'app-manage-contest',
    templateUrl: './manage-contest.component.html',
    styleUrls: [ './manage-contest.component.scss' ]
} )
export class ManageContestComponent
{
    constructor( private route: ActivatedRoute, private router: Router, private tasksService: TasksService )
    {
        this.route.paramMap.subscribe( paramMap =>
        {
            const baseContestId = Number( paramMap.get( 'baseContestId' ) )
            const compositeContestId = Number( paramMap.get( 'compositeContestId' ) )
            this.stageId = Number( paramMap.get( 'stageId' ) )
            if ( !!this.stageId )
            {
                this.tasksService.tasksUnauthorizedOlympiadIdOlympiadStageIdStageGet( compositeContestId, this.stageId ).subscribe( response =>
                {
                    this.stage = response
                } )
            }
        } )
    }

    stageId!: number
    stage!: Stage

    @ViewChild( DxDataGridComponent, { static: false } ) grid!: DxDataGridComponent
    selectedRowIndex: number = -1
    selectedRow?: SimpleContest = undefined

    navigateElement(): void
    {
        if ( this.selectedRow )
        {
            const routePath = [ '/manage', 'contests', this.selectedRow.base_contest.base_contest_id, 'contest', this.selectedRow.contest_id, 'users' ]
            this.router.navigate( routePath )
        }
    }

    navigateElement2(): void
    {
        if ( this.selectedRow )
        {
            const routePath = [ '/manage', 'contests', this.selectedRow.base_contest.base_contest_id, 'contest', this.selectedRow.contest_id, 'variants' ]
            this.router.navigate( routePath )
        }
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
