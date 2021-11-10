import { Component, ViewChild } from '@angular/core'
import { CompositeContest, Stage } from '@api/tasks/model'
import { ActivatedRoute, Router } from '@angular/router'
import { TasksService } from '@api/tasks/tasks.service'
import { DxDataGridComponent } from 'devextreme-angular'


@Component( {
    selector: 'app-manage-composite-contest-stages',
    templateUrl: './manage-composite-contest-stages.component.html',
    styleUrls: [ './manage-composite-contest-stages.component.scss' ]
} )
export class ManageCompositeContestStagesComponent
{
    constructor( private route: ActivatedRoute, private router: Router, private tasksService: TasksService )
    {
        this.route.paramMap.subscribe( paramMap =>
        {
            const baseContestId = Number( paramMap.get( 'baseContestId' ) )
            this.compositeContestId = Number( paramMap.get( 'compositeContestId' ) )
            if ( !!this.compositeContestId )
            {
                this.tasksService.tasksUnauthorizedBaseOlympiadIdBaseOlympiadOlympiadIdOlympiadGet( baseContestId, this.compositeContestId ).subscribe( response =>
                {
                    this.compositeContest = response as CompositeContest
                } )
            }
        } )
    }

    compositeContestId!: number
    compositeContest!: CompositeContest

    @ViewChild( DxDataGridComponent, { static: false } ) grid!: DxDataGridComponent
    selectedRowIndex: number = -1
    selectedRow?: Stage = undefined
    stageConditionEnum = Object.values( Stage.ConditionEnum )

    navigateToSelected(): void
    {
        if ( this.selectedRow )
            this.router.navigate( [ this.selectedRow.stage_id ], { relativeTo: this.route } )
    }

    addElement(): void
    {
        this.grid.instance.addRow()
        this.grid.instance.deselectAll()
    }

    editElement(): void
    {
        this.grid.instance.editRow( this.selectedRowIndex )
        this.grid.instance.deselectAll()
    }


    selectedChanged( $event: any ): void
    {
        this.selectedRow = $event.selectedRowsData[ 0 ]
        this.selectedRowIndex = $event.component.getRowIndexByKey( $event.selectedRowKeys[ 0 ] )
    }
}