import { Component, ViewChild } from '@angular/core'
import { ActivatedRoute, Router } from '@angular/router'
import { TasksService } from '@api/tasks/tasks.service'
import { Variant } from '@api/tasks/model'
import { DxDataGridComponent } from 'devextreme-angular'


@Component( {
    selector: 'app-manage-contest-variants',
    templateUrl: './manage-contest-variants.component.html',
    styleUrls: [ './manage-contest-variants.component.scss' ]
} )
export class ManageContestVariantsComponent
{
    constructor( private route: ActivatedRoute, private router: Router, private tasksService: TasksService )
    {
        this.route.paramMap.subscribe( paramMap =>
        {
            this.simpleContestId = Number( paramMap.get( 'simpleContestId' ) )
            if ( !!this.simpleContestId )
            {
                this.tasksService.tasksCreatorContestIdContestVariantAllGet( this.simpleContestId ).subscribe( response =>
                {
                    this.variants = response.variants_list
                } )
            }
        } )
    }


    simpleContestId!: number
    variants: Array<Variant> = []

    @ViewChild( DxDataGridComponent, { static: false } ) grid!: DxDataGridComponent
    selectedRowIndex: number = -1
    selectedRow?: Variant = undefined

    navigateElement(): void
    {
        if ( this.selectedRow )
            this.router.navigate( [ this.selectedRow.variant_id, 'tasks' ], { relativeTo: this.route } )
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