import { Component, ViewChild } from '@angular/core'
import { ActivatedRoute, Router } from '@angular/router'
import { TasksService } from '@api/tasks/tasks.service'
import { PlainTask } from '@api/tasks/model'
import { DxDataGridComponent } from 'devextreme-angular'


@Component( {
    selector: 'app-manage-contest-variant-tasks',
    templateUrl: './manage-contest-variant-tasks.component.html',
    styleUrls: [ './manage-contest-variant-tasks.component.scss' ]
} )
export class ManageContestVariantTasksComponent
{
    constructor( private route: ActivatedRoute, private router: Router, private tasksService: TasksService )
    {
        this.route.paramMap.subscribe( paramMap =>
        {
            const simpleContestId = Number( paramMap.get( 'simpleContestId' ) )
            this.variantId = Number( paramMap.get( 'variantId' ) )
            if ( !!simpleContestId && !!this.variantId )
            {
                // TODO method tasksCreatorContestIdContestVariantIdVariantTaskAllGet removed
                // this.tasksService.tasksCreatorContestIdContestVariantIdVariantTaskAllGet( simpleContestId, this.variantId ).subscribe( response =>
                // {
                //     this.tasks = response.tasks_list as PlainTask[]
                // } )
            }
        } )
    }


    variantId!: number
    tasks: Array<PlainTask> = []

    @ViewChild( DxDataGridComponent, { static: false } ) grid!: DxDataGridComponent
    selectedRowIndex: number = -1
    selectedRow?: PlainTask = undefined

    navigateElement(): void
    {
        // if ( this.selectedRow )
        //     this.router.navigate( [ this.selectedRow.variant_id, 'tasks' ], { relativeTo: this.route } )
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
