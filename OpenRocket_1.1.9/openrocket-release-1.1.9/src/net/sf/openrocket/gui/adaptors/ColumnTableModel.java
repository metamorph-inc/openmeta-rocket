package net.sf.openrocket.gui.adaptors;

import javax.swing.table.AbstractTableModel;
import javax.swing.table.TableColumn;
import javax.swing.table.TableColumnModel;

import net.sf.openrocket.gui.main.ExceptionHandler;

public abstract class ColumnTableModel extends AbstractTableModel {
	private final Column[] columns;
	
	public ColumnTableModel(Column... columns) {
		this.columns = columns;
	}
	
	public void setColumnWidths(TableColumnModel model) {
		for (int i = 0; i < columns.length; i++) {
			if (columns[i].getExactWidth() > 0) {
				TableColumn col = model.getColumn(i);
				int w = columns[i].getExactWidth();
				col.setResizable(false);
				col.setMinWidth(w);
				col.setMaxWidth(w);
				col.setPreferredWidth(w);
			} else {
				model.getColumn(i).setPreferredWidth(columns[i].getDefaultWidth());
			}
		}
	}
	
	@Override
	public int getColumnCount() {
		return columns.length;
	}
	
	@Override
	public String getColumnName(int col) {
		return columns[col].toString();
	}
	
	@Override
	public Class<?> getColumnClass(int col) {
		return columns[col].getColumnClass();
	}
	
	@Override
	public Object getValueAt(int row, int col) {
		if ((row < 0) || (row >= getRowCount()) ||
				(col < 0) || (col >= columns.length)) {
			ExceptionHandler.handleErrorCondition("Error:  Requested illegal column/row, col=" + col + " row=" + row);
			return null;
		}
		return columns[col].getValueAt(row);
	}
	
}
